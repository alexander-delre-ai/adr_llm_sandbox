#!/usr/bin/env python3
"""
Daily Chat Keyword Insights Extractor

Parses Cursor agent transcripts (.jsonl) and Slack messages (JSON) to extract:
- Topics & technologies (domain keywords, JIRA keys, file paths, tools)
- Questions asked (with resolution status)
- Debugging sessions (errors, retries, fixes)
- Recurring themes (cross-day trends from previous reports)

Usage:
    python3 extract_keywords.py [--date YYYY-MM-DD] [--transcripts-dir DIR] [--slack-file FILE] [--insights-dir DIR] [--claude-file FILE]
"""

import argparse
import json
import re
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
DEFAULT_INSIGHTS_DIR = Path.home() / "adr_llm_sandbox/insights"

WORKSPACE_TRANSCRIPT_DIRS = {
    "adr-llm-sandbox": Path.home() / ".cursor/projects/home-alexanderdelre-adr-llm-sandbox/agent-transcripts",
    "core-stack": Path.home() / ".cursor/projects/home-alexanderdelre-applied-core-stack/agent-transcripts",
    "vehicle-os-katana": Path.home() / ".cursor/projects/home-alexanderdelre-applied-vehicle-os-katana/agent-transcripts",
}

JIRA_FULL_KEY_RE = re.compile(r"\b(KATA-\d+|AVP-\d+)\b")

STRIP_BLOCK_TAGS = {
    "attached_files", "code_selection", "system_reminder",
    "manually_attached_skills", "external_links", "image_files",
    "agent_skills", "available_skills", "agent_skill",
    "rules", "always_applied_workspace_rules", "always_applied_workspace_rule",
    "open_and_recently_viewed_files", "git_status", "user_info",
    "mcp_file_system", "mcp_file_system_servers", "mcp_file_system_server",
    "tone_and_style", "tool_calling", "making_code_changes", "citing_code",
    "terminal_files_information", "task_management", "inline_line_numbers",
    "mode_selection", "linter_errors", "no_thinking_in_code_or_commands",
    "committing-changes-with-git", "creating-pull-requests",
    "other-common-operations", "managing-long-running-commands",
    "mermaid_syntax", "agent_transcripts", "system-communication",
}
OPEN_TAG_RE = re.compile(r"<(" + "|".join(re.escape(t) for t in STRIP_BLOCK_TAGS) + r")(?:\s[^>]*)?>", re.IGNORECASE)
CLOSE_TAG_RE = re.compile(r"</(" + "|".join(re.escape(t) for t in STRIP_BLOCK_TAGS) + r")>", re.IGNORECASE)
XML_TAG_RE = re.compile(r"</?(?:user_query|" + "|".join(re.escape(t) for t in STRIP_BLOCK_TAGS) + r")[^>]*>", re.IGNORECASE)
JIRA_KEY_RE = re.compile(r"\b(KATA|AVP)-\d+\b")
FILE_PATH_RE = re.compile(r"(?:^|[\s\"'`(])(/[\w./-]+\.(?:py|sh|md|json|ts|tsx|js|yaml|yml|toml))\b")
MCP_TOOL_RE = re.compile(r"\b(mcp__[\w-]+__\w+|slack_\w+|createJiraIssue|editJiraIssue|createIssueLink|getIssueLinkTypes|lookupJiraAccountId|getAccessibleAtlassianResources)\b")
ERROR_PATTERNS = re.compile(
    r"(?:"
    r"(?:exit\s+code|status\s+code|returned?)\s*:?\s*[1-9]\d*|"  # exit code: N
    r"\bTraceback\s*\(|"                                           # Python traceback
    r"\bException\b.*:|"                                           # Exception: message
    r"\bERROR\b|"                                                  # uppercase ERROR (log lines)
    r"\bfailed\s+(?:to|with)|"                                     # "failed to X" / "failed with"
    r"\bretry(?:ing)?\b|"                                          # retry / retrying
    r"\bInvalid\s+\w+|"                                            # "Invalid ADF", "Invalid field"
    r"\bnot\s+found\b|"                                            # "not found"
    r"\btimed?\s*out\b|"                                           # timeout
    r"\b(?:403|404|500|502|503)\b"                                 # HTTP error codes
    r")"
)
HEDGING_PHRASES = re.compile(r"(?:I'm not sure|I don't know|I cannot|I can't determine|unclear|not certain|hard to say)", re.IGNORECASE)
INTERROGATIVE_RE = re.compile(r"\b(?:how\s+(?:do|does|can|should|would|is|are|to)|where\s+(?:is|are|do|does|can)|what\s+(?:is|are|does|do|should|would|happens)|why\s+(?:is|are|does|do|did|would)|which\s+(?:is|are|one)|can\s+(?:we|you|i|it)|does\s+(?:it|this|the|that)|is\s+(?:there|it|this|that)|do\s+(?:we|you|i)|should\s+(?:we|i|it))\b", re.IGNORECASE)


def load_domain_keywords():
    kw_file = DATA_DIR / "domain-keywords.json"
    if not kw_file.exists():
        return {}
    with open(kw_file) as f:
        return json.load(f)


def strip_xml_tags(text):
    """Remove system metadata XML blocks and tags using a state machine."""
    result_lines = []
    skip_depth = 0
    for line in text.split("\n"):
        for m in OPEN_TAG_RE.finditer(line):
            skip_depth += 1
        for m in CLOSE_TAG_RE.finditer(line):
            skip_depth = max(0, skip_depth - 1)

        if skip_depth == 0 and not CLOSE_TAG_RE.search(line):
            cleaned = XML_TAG_RE.sub("", line)
            if cleaned.strip():
                result_lines.append(cleaned)

    return "\n".join(result_lines).strip()


def extract_text_from_content(content_list):
    parts = []
    for item in content_list:
        if item.get("type") == "text":
            raw = item.get("text", "")
            parts.append(strip_xml_tags(raw))
    return " ".join(parts).strip()


def parse_transcript(filepath):
    """Parse a .jsonl transcript into a list of (role, text) turns."""
    turns = []
    with open(filepath) as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            role = obj.get("role", "unknown")
            content = obj.get("message", {}).get("content", [])
            text = extract_text_from_content(content)
            if text:
                turns.append((role, text))
    return turns


def parse_slack_messages(filepath):
    """Parse Slack messages exported as JSON array of {text, user, ts, ...}."""
    if not filepath or not Path(filepath).exists():
        return []
    with open(filepath) as f:
        data = json.load(f)
    messages = []
    if isinstance(data, list):
        for msg in data:
            text = msg.get("text", "")
            user = msg.get("user", "unknown")
            if text:
                messages.append(("user", text))
    elif isinstance(data, dict) and "messages" in data:
        for msg in data["messages"]:
            text = msg.get("text", "")
            if text:
                messages.append(("user", text))
    return messages


def parse_claude_chat(filepath):
    """Parse a plain-text Claude chat file (alternating Human:/Assistant: blocks)."""
    if not filepath or not Path(filepath).exists():
        return []
    with open(filepath) as f:
        content = f.read()
    turns = []
    blocks = re.split(r"\n(?=(?:Human|Assistant|H|A):)", content)
    for block in blocks:
        block = block.strip()
        if block.startswith(("Human:", "H:")):
            turns.append(("user", re.sub(r"^(?:Human|H):\s*", "", block)))
        elif block.startswith(("Assistant:", "A:")):
            turns.append(("assistant", re.sub(r"^(?:Assistant|A):\s*", "", block)))
        elif block:
            turns.append(("user", block))
    return turns


def find_todays_transcripts(transcripts_dir, target_date):
    """Find transcript files modified on target_date."""
    found = []
    base = Path(transcripts_dir)
    if not base.exists():
        return found
    for session_dir in base.iterdir():
        if not session_dir.is_dir():
            continue
        jsonl = session_dir / f"{session_dir.name}.jsonl"
        if not jsonl.exists():
            continue
        mtime = datetime.fromtimestamp(jsonl.stat().st_mtime).date()
        if mtime == target_date:
            found.append(jsonl)
    return sorted(found, key=lambda p: p.stat().st_mtime)


def extract_topics(all_text, domain_keywords):
    """Extract topics and technologies from combined text (excluding JIRA keys)."""
    topics = Counter()

    for category, terms in domain_keywords.items():
        for term in terms:
            pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
            matches = pattern.findall(all_text)
            if matches:
                topics[term] += len(matches)

    canonical_map = {}
    for term in list(topics.keys()):
        lower = term.lower()
        if lower not in canonical_map:
            canonical_map[lower] = term
        elif topics[term] > topics[canonical_map[lower]]:
            canonical_map[lower] = term

    merged = Counter()
    for term, count in topics.items():
        canonical = canonical_map[term.lower()]
        merged[canonical] += count
    topics = merged

    mcp_tools = MCP_TOOL_RE.findall(all_text)
    for tool in mcp_tools:
        topics[tool] += 1

    return topics


def extract_jira_tickets(all_text):
    """Extract JIRA ticket keys and their mention counts."""
    return Counter(JIRA_FULL_KEY_RE.findall(all_text))


def extract_all_by_source(sources_data, domain_keywords):
    """Extract topics and JIRA tickets with source attribution."""
    global_topics = Counter()
    global_jira = Counter()
    topic_attribution = defaultdict(set)
    jira_attribution = defaultdict(set)

    for source_id, text in sources_data:
        topics = extract_topics(text, domain_keywords)
        for term, count in topics.items():
            global_topics[term] += count
            topic_attribution[term].add(source_id)

        jira = extract_jira_tickets(text)
        for key, count in jira.items():
            global_jira[key] += count
            jira_attribution[key].add(source_id)

    return global_topics, topic_attribution, global_jira, jira_attribution


NOISE_PATTERNS = re.compile(
    r"(?:"
    r"^\d+/|"                     # line-numbered content (1/---, 2/name:)
    r"^---\s*$|"                  # YAML frontmatter delimiters
    r"^```|"                      # code fences
    r"^\s*\|.*\|.*\||"           # markdown table rows
    r"^name:|^overview:|^todos:|" # plan frontmatter fields
    r"^#\s|"                      # markdown headings
    r"https?://\S{50,}|"         # long URLs
    r"^@\."                       # @-file references
    r")",
    re.MULTILINE,
)


def extract_questions(turns, source_id):
    """Find questions in user messages and check if resolved."""
    questions = []
    for i, (role, text) in enumerate(turns):
        if role != "user":
            continue
        if "?" not in text and not INTERROGATIVE_RE.search(text):
            continue

        sentences = re.split(r"[.!?\n]+", text)
        q_sentences = []
        for s in sentences:
            s = s.strip()
            if len(s) < 15 or len(s) > 300:
                continue
            if NOISE_PATTERNS.search(s):
                continue
            if "?" in s or INTERROGATIVE_RE.search(s):
                q_sentences.append(s)

        if not q_sentences:
            continue

        assistant_responses = []
        for j in range(i + 1, min(i + 5, len(turns))):
            if turns[j][0] == "user":
                break
            assistant_responses.append(turns[j][1])
        combined_response = " ".join(assistant_responses)

        resolved = (
            len(combined_response) > 100
            and not HEDGING_PHRASES.search(combined_response)
        )

        for q in q_sentences:
            questions.append({
                "question": q[:200],
                "source": source_id,
                "resolved": resolved,
            })

    return questions


def extract_debug_sessions(turns, source_id):
    """Detect debugging/error sessions from conversation turns."""
    sessions = []
    current_session = None

    for i, (role, text) in enumerate(turns):
        has_error = bool(ERROR_PATTERNS.search(text))

        if has_error:
            if current_session is None:
                current_session = {
                    "start_idx": i,
                    "issues": [],
                    "context_turns": [],
                    "source": source_id,
                }

            error_matches = ERROR_PATTERNS.findall(text)
            snippet = text[:300].strip()
            current_session["issues"].extend(error_matches[:3])
            current_session["context_turns"].append((role, snippet))
        else:
            if current_session is not None:
                if role == "assistant" and len(text) > 50:
                    current_session["resolution"] = text[:300].strip()
                sessions.append(current_session)
                current_session = None

    if current_session:
        sessions.append(current_session)

    results = []
    for session in sessions:
        unique_issues = list(dict.fromkeys(session["issues"]))[:5]
        issue_desc = ", ".join(unique_issues)
        context = session["context_turns"][0][1][:150] if session["context_turns"] else ""
        resolution = session.get("resolution", "")[:150]

        results.append({
            "issue": issue_desc,
            "context": context,
            "resolution": resolution if resolution else "Unresolved",
            "source": session["source"],
        })

    return results


def load_historical_keywords(insights_dir, target_date, lookback_days=7):
    """Load keywords from previous daily reports for trend analysis."""
    historical = defaultdict(list)
    base = Path(insights_dir)
    if not base.exists():
        return historical

    for day_offset in range(1, lookback_days + 1):
        past_date = target_date - timedelta(days=day_offset)
        report_file = base / f"{past_date.isoformat()}.md"
        if not report_file.exists():
            continue

        with open(report_file) as f:
            content = f.read()

        in_topics = False
        for line in content.split("\n"):
            if "## Topics & Technologies" in line:
                in_topics = True
                continue
            if in_topics and line.startswith("##"):
                break
            if in_topics and line.startswith("| ") and not line.startswith("| Keyword"):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 3:
                    keyword = parts[1]
                    if keyword and keyword != "---":
                        historical[keyword].append(past_date.isoformat())

    return historical


def compute_recurring_themes(today_topics, historical, lookback_days=7):
    """Find keywords appearing 3+ days in the last week."""
    themes = []
    for keyword in today_topics:
        past_days = historical.get(keyword, [])
        total_days = len(past_days) + 1
        if total_days >= 3:
            if len(past_days) >= 2:
                trend = "steady"
            elif len(past_days) >= 1:
                trend = "rising"
            else:
                trend = "new"
            themes.append({
                "theme": keyword,
                "days": total_days,
                "max_days": lookback_days,
                "trend": trend,
            })

    themes.sort(key=lambda x: x["days"], reverse=True)
    return themes


def summarize_session(transcript_path, turns, workspace_name=""):
    """Generate a brief summary for one transcript session."""
    session_id = transcript_path.stem[:8]
    total_turns = len(turns)
    user_turns = [t for r, t in turns if r == "user"]

    first_query = ""
    for _, text in turns:
        cleaned = text.strip()
        if cleaned and len(cleaned) > 10:
            first_query = cleaned[:100]
            break

    return {
        "session_id": session_id,
        "full_id": transcript_path.stem,
        "workspace": workspace_name,
        "total_turns": total_turns,
        "user_turns": len(user_turns),
        "first_query": first_query,
    }


JIRA_BASE_URLS = {
    "KATA": "https://appliedint-katana.atlassian.net/browse",
    "AVP": "https://appliedint.atlassian.net/browse",
}


def generate_report(date_str, sources_count, topics, topic_attribution,
                     jira_tickets, jira_attribution,
                     questions, debug_sessions, recurring_themes,
                     session_summaries):
    """Generate the markdown report."""
    lines = []
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    human_date = dt.strftime("%B %d, %Y")

    lines.append(f"# Chat Insights - {human_date}")
    lines.append("")

    lines.append("## Sources")
    for src_type, count in sources_count.items():
        lines.append(f"- {src_type}: {count}")
    lines.append("")

    lines.append("## JIRA Tickets")
    lines.append("| Ticket | Count | Sources |")
    lines.append("|--------|-------|---------|")
    for key, count in jira_tickets.most_common(30):
        prefix = key.split("-")[0]
        base_url = JIRA_BASE_URLS.get(prefix, "")
        link = f"[{key}]({base_url}/{key})" if base_url else key
        srcs = ", ".join(sorted(jira_attribution.get(key, set())))
        lines.append(f"| {link} | {count} | {srcs} |")
    if not jira_tickets:
        lines.append("| (none) | - | - |")
    lines.append("")

    lines.append("## Topics & Technologies")
    lines.append("| Keyword | Count | Sources |")
    lines.append("|---------|-------|---------|")
    for keyword, count in topics.most_common(30):
        srcs = ", ".join(sorted(topic_attribution.get(keyword, set())))
        lines.append(f"| {keyword} | {count} | {srcs} |")
    lines.append("")

    lines.append("## Questions")
    lines.append("| Question | Source | Status |")
    lines.append("|----------|--------|--------|")
    seen = set()
    for q in questions:
        q_text = q["question"].replace("|", "/")
        if q_text in seen:
            continue
        seen.add(q_text)
        status = "Resolved" if q["resolved"] else "Open"
        lines.append(f"| {q_text} | {q['source']} | {status} |")
    lines.append("")

    lines.append("## Debugging & Errors")
    lines.append("| Issue | Context | Resolution |")
    lines.append("|-------|---------|------------|")
    for d in debug_sessions:
        issue = d["issue"].replace("|", "/")
        ctx = d["context"].replace("|", "/").replace("\n", " ")[:100]
        res = d["resolution"].replace("|", "/").replace("\n", " ")[:100]
        lines.append(f"| {issue} | {ctx} | {res} |")
    if not debug_sessions:
        lines.append("| (none) | - | - |")
    lines.append("")

    lines.append("## Recurring Themes (last 7 days)")
    lines.append("| Theme | Days | Trend |")
    lines.append("|-------|------|-------|")
    for t in recurring_themes:
        lines.append(f"| {t['theme']} | {t['days']}/{t['max_days']} | {t['trend']} |")
    if not recurring_themes:
        lines.append("| (none yet - trends appear after 3+ days of data) | - | - |")
    lines.append("")

    lines.append("## Session Summaries")
    for s in session_summaries:
        ws_label = f" ({s['workspace']})" if s.get("workspace") else ""
        lines.append(f"### [{s['session_id']}]{ws_label} {s['first_query']}")
        lines.append(f"- {s['total_turns']} turns ({s['user_turns']} user messages)")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Extract keywords from daily chat activity")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"),
                        help="Target date (YYYY-MM-DD, default: today)")
    parser.add_argument("--extra-transcripts-dir", action="append", default=[],
                        help="Additional transcript dirs as name:path (can repeat)")
    parser.add_argument("--slack-file", default=None,
                        help="Path to JSON file with Slack messages")
    parser.add_argument("--claude-file", default=None,
                        help="Path to plain-text Claude chat export")
    parser.add_argument("--insights-dir", default=str(DEFAULT_INSIGHTS_DIR),
                        help="Output directory for reports")
    parser.add_argument("--stdout", action="store_true",
                        help="Print report to stdout instead of writing to file")
    args = parser.parse_args()

    target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    insights_dir = Path(args.insights_dir)
    insights_dir.mkdir(parents=True, exist_ok=True)

    domain_keywords = load_domain_keywords()
    sources_count = {}

    all_sources_data = []
    all_questions = []
    all_debug_sessions = []
    session_summaries = []

    workspace_dirs = dict(WORKSPACE_TRANSCRIPT_DIRS)
    for extra in args.extra_transcripts_dir:
        if ":" in extra:
            name, path = extra.split(":", 1)
            workspace_dirs[name] = Path(path)

    total_transcripts = 0
    for ws_name, ws_dir in workspace_dirs.items():
        transcripts = find_todays_transcripts(str(ws_dir), target_date)
        if not transcripts:
            continue
        total_transcripts += len(transcripts)
        sources_count[f"  {ws_name}"] = f"{len(transcripts)} sessions"

        for t_path in transcripts:
            source_id = f"{ws_name}:{t_path.stem[:8]}"
            turns = parse_transcript(t_path)
            if not turns:
                continue

            full_text = " ".join(text for _, text in turns)
            all_sources_data.append((source_id, full_text))
            all_questions.extend(extract_questions(turns, source_id))
            all_debug_sessions.extend(extract_debug_sessions(turns, source_id))
            session_summaries.append(summarize_session(t_path, turns, ws_name))

    final_sources = {"Agent transcripts": f"{total_transcripts} sessions across {len(workspace_dirs)} workspaces"}
    for k, v in sources_count.items():
        final_sources[k] = v

    if args.slack_file:
        slack_turns = parse_slack_messages(args.slack_file)
        final_sources["Slack #ext-program-katana-sdv"] = f"{len(slack_turns)} messages scanned"
        if slack_turns:
            full_text = " ".join(text for _, text in slack_turns)
            all_sources_data.append(("slack", full_text))
            all_questions.extend(extract_questions(slack_turns, "slack"))
            all_debug_sessions.extend(extract_debug_sessions(slack_turns, "slack"))

    if args.claude_file:
        claude_turns = parse_claude_chat(args.claude_file)
        final_sources["Claude chats"] = f"{len(claude_turns)} turns processed"
        if claude_turns:
            full_text = " ".join(text for _, text in claude_turns)
            all_sources_data.append(("claude", full_text))
            all_questions.extend(extract_questions(claude_turns, "claude"))
            all_debug_sessions.extend(extract_debug_sessions(claude_turns, "claude"))

    topics, topic_attribution, jira_tickets, jira_attribution = extract_all_by_source(
        all_sources_data, domain_keywords
    )

    historical = load_historical_keywords(insights_dir, target_date)
    recurring_themes = compute_recurring_themes(topics, historical)

    report = generate_report(
        args.date, final_sources, topics, topic_attribution,
        jira_tickets, jira_attribution,
        all_questions, all_debug_sessions, recurring_themes,
        session_summaries
    )

    if args.stdout:
        print(report)
    else:
        output_file = insights_dir / f"{args.date}.md"
        with open(output_file, "w") as f:
            f.write(report)
        print(f"Report written to {output_file}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
