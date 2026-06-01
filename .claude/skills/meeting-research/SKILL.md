---
name: meeting-research
description: Searches Slack, Confluence, Google Drive, JIRA, and configured codebases to answer questions arising from meetings. Takes a question and optional meeting context, runs multi-source searches, and synthesizes findings into a structured response with sources. Use when researching unresolved questions, looking up prior decisions, or finding implementation details related to meeting discussions.
---

# Meeting Research

Searches prior meeting workspaces, Slack, Confluence (Applied + KATA), Google Drive, JIRA (AVP + KATA), and local codebases to find answers to questions from meeting discussions. Produces a structured response with synthesized answer, sources, and identified gaps.

**MCP naming**: Use whichever Atlassian and Slack MCP tools your session exposes. This document uses illustrative server names (`user-Slack`, `user-atlassian-mcp-applied`, `user-atlassian-mcp-kata`); in Claude Code, these often appear as `mcp__kata-atlassian__*`, `mcp__claude_ai_Slack__*`, etc. Prefer the tools listed in `CLAUDE.md` at the repository root when names differ.

**Codebase config**: Local repos to search are defined in `codebases.yaml` (same directory as this file). Read that file at the start of any session that may involve codebase search so you have the current path and tag list.

## Classification: Research vs. Skip

Before running any searches, classify each question. Apply this classification in `meeting-plan` Step 8 before invoking this skill.

**Skip ONLY if the question is one of these two types:**
1. **Org coordination / intro brokering**: "What should Person A share with Person B?", "Who should be introduced to whom?", "What is the coordination model between X and Y?"
2. **Scheduling or logistics**: "Is next sprint feasible?", "Who attends the next meeting?", "When should we schedule the follow-up?"

**Everything else defaults to Research**, including:
- Questions that require code inspection (search the codebase)
- Questions that require a person to check and report back (search Slack for prior discussion first)
- Questions that require a live demo (search for docs or prior Slack threads about the feature)
- Technical architecture questions, implementation details, API design
- Process questions about how a tool or system works

**Ambiguous cases**: Default to Research. Running a search and finding nothing is a better outcome than skipping without looking.

**Mandatory search rule**: For every Research-classified question, at least one actual MCP search must be run before the question can be marked Open or unanswered. Hypothesis-only answers are not permitted.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| question | Yes | The specific question to research |
| context | No | Meeting workspace path (e.g., `workspaces/2026-03-13/sdv-sw-oh`) or inline background context |
| scope | No | Comma-separated source list: `workspaces`, `slack`, `confluence`, `drive`, `jira`, `codebase`. Defaults to all. |

## Workflow

### Step 1: Parse question, load context, and search prior workspaces

- Extract key technical terms and entities from the question.
- Generate 2-4 keyword search variants:
  - **Broad**: core nouns and verbs (e.g., "current draw HSD efuse")
  - **Narrow**: exact phrases or specific terms (e.g., "current readback HSD application")
  - **Synonym**: alternate terminology (e.g., "efuse current feedback software")
- **Load meeting context**: If a workspace path is provided, read `analysis.md` and `transcript.md` for background.
- **Search prior workspaces**: Scan `analysis.md` files in `workspaces/` for the same keywords using Glob + Read. This surfaces whether the question (or a closely related one) was discussed or answered in a prior session. Treat findings as context that informs the external searches but do not substitute for them — always also run Steps 2-4.

### Step 2: Search Slack

Use your configured Slack MCP.

- Run 2-3 parallel searches using `slack_search_public_and_private`:
  - `query: "<keyword variant>"`
  - `sort: "timestamp"`
  - `sort_dir: "desc"`
  - `include_context: true`
  - `limit: 10`
- For promising thread results, follow up with `slack_read_thread` to get full context.
- Deduplicate results across query variants by `message_ts`.

### Step 3: Search Confluence + Google Drive (in parallel)

Run Confluence and Google Drive searches concurrently since both are document stores.

#### Confluence (Applied first, then KATA)

**Applied Confluence** (cloudId: `6461690f-d275-4167-8055-cc3dc06e03f2`):

- Preferred: `searchAtlassian` with natural language query (Rovo Search)
- Fallback: `searchConfluenceUsingCql` for precise queries:
  - `cql: "text ~ \"term1\" AND text ~ \"term2\" AND type = page"`
  - `limit: 10`
- Key spaces: AVP (Applied Vehicle Platform), ONSP (Solution Engineering)

**KATA Confluence** (cloudId: `eadd00c6-0d3f-4c89-99e3-ad95a0daaa51`):

- Same dual approach: `searchAtlassian` first, CQL if needed
- Key spaces: KAN (Project Katana): meeting notes, customer-facing docs

For promising results, fetch full page content with `getConfluencePage` using the page ID from search results.

#### Google Drive (parallel with Confluence)

Use `mcp__google-drive__search` (keyword search). Target all file types: Docs, Sheets, Slides.

- Run 2 keyword searches in parallel using the broad and narrow variants from Step 1.
- Deduplicate results by file ID across queries.
- For promising Docs or Sheets, fetch content with `mcp__google-drive__getGoogleDocContent` or `mcp__google-drive__getGoogleSheetContent`.
- Skip fetching Slides content unless a deck title is directly relevant; note its existence and link instead.

### Step 4: Search JIRA (Applied first, then KATA)

**Applied JIRA (AVP)** (cloudId: `6461690f-d275-4167-8055-cc3dc06e03f2`):

- `searchJiraIssuesUsingJql` with JQL such as: `text ~ "term1" AND text ~ "term2" ORDER BY created DESC`
- `maxResults: 10`
- Request fields: summary, description, status, priority, assignee

**KATA JIRA** (cloudId: `eadd00c6-0d3f-4c89-99e3-ad95a0daaa51`):

- Same approach on the KATA project.

### Step 5: Search codebases

**When to search**: Always search the codebase when:
- The question is about VehicleOS internal behavior, implementation, or configuration (e.g., "does PDU runnable handle periodic broadcast?")
- The question references a specific system, component, or driver even without naming a file or function
- The question is about API design, signal injection, test framework mechanics, or PyArch behavior

Skip codebase search only for pure process, scheduling, or coordination questions.

**Codebase list**: Read `codebases.yaml` in the same directory as this skill file before running any codebase searches.

**Routing**: For each repo in `codebases.yaml`, check whether any of its `tags` overlap with the question's key terms. Search repos where there is tag overlap, or all repos when the question is cross-cutting.

For each matching repo:
- Semantic search with `target_directories` set to that repo for broad questions
- `Grep` with `path` set to that repo for symbol or function lookups
- `Glob` with `target_directory` set to that repo for file patterns

When results come from multiple repos, attribute each finding to its source repo by path.

### Step 6: Synthesize and present findings

- Provide a **consolidated answer** at the top that directly addresses the question.
- Group supporting findings by source (Prior Workspaces, Slack, Confluence, Drive, JIRA, Codebase).
- For each finding: short summary, direct link or permalink, date, and relevance note.
- Flag contradictions or gaps across sources.
- **Escalation hint**: If the question remains unresolved and the meeting transcript named a specific person or team responsible for the answer, surface that: "Follow up with <Person>." Do not invent suggestions not grounded in the meeting context.
- Omit source sections that returned no results.

## Output Format

### Standalone usage (single question)

```markdown
## Research: <question summary>

### Answer
<Direct synthesized answer citing sources>

### Prior Workspaces
- **<workspace slug>** (<date>): <summary of what was discussed>
  - Relevance: <why this matters>

### Slack
- **<channel or DM name>** (<date>): <summary> [link]
  - Relevance: <why this matters>

### Confluence
- **<page title>** (<space>, <last modified>): <summary> [link]
  - Relevance: <why this matters>

### Google Drive
- **<file name>** (<file type>, <last modified>): <summary> [link]
  - Relevance: <why this matters>

### JIRA
- **<TICKET-KEY>**: <summary>, Status: <status> [link]
  - Relevance: <why this matters>

### Codebase (if applicable)
- **<repo>/<file path>**: <what was found>
  - Relevance: <why this matters>

### Gaps / Follow-up
- <unresolved aspects or suggested next steps>
- Follow up with <Person> [only if named in the meeting transcript]
```

### Batch usage (meeting-plan integration)

When called from `meeting-plan` against multiple unresolved questions, compile results into a single `research.md`:

```markdown
# Research: <Meeting Title> (<Date>)

Generated from unresolved questions in analysis.md, Section 4.

---

## Q1: <question text>

### Answer
<synthesized answer>

### Sources
- **Slack**: <findings with links>
- **Confluence**: <findings with links>
- **Google Drive**: <findings with links>
- **JIRA**: <findings with links>
- **Codebase**: <findings if applicable, attributed per repo>
- **Prior Workspaces**: <findings if applicable>

### Gaps
- <unresolved aspects>
- Follow up with <Person> [only if named in the meeting transcript]

---

## Q2: <next question>
[repeat structure]
```

Omit empty source sections. If a question yields no results from any source, state "No relevant results found across all sources" and list the search terms that were tried.

## Rules

- **Parallel searches**: Run Slack, Confluence+Drive, and JIRA searches in parallel where possible; Confluence and Drive always run concurrently.
- **Prior workspaces first**: Scan prior workspace files before hitting external APIs to establish context, but always run external searches regardless of workspace findings.
- **Applied first**: Always search Applied or AVP spaces before KATA spaces in Confluence and JIRA when both apply.
- **Mandatory search**: At least one MCP search must run per Research-classified question before it can be marked Open or unanswered.
- **Deduplication**: Same content found via multiple queries appears only once; deduplicate Drive results by file ID.
- **Source links**: Always include permalinks or URLs so the user can verify findings.
- **Relevance filtering**: Exclude results that mention search terms but are clearly unrelated to the question context.
- **Large results**: If a Confluence page is relevant, fetch full content with `getConfluencePage`; for Drive Docs/Sheets fetch content when the file name indicates high relevance.
- **Codebase**: Search codebase for any VehicleOS-internal technical question, not just those naming a specific file or function.
- **Codebase config**: Always read `codebases.yaml` before running codebase searches so paths and tags are current.
- **Multi-repo attribution**: When codebase results span repos, label each finding with its source repo path.
- **Escalation hints**: Surface follow-up person/channel only when the meeting transcript explicitly named who owns the answer. Do not fabricate suggestions.
- **No hypothesis-only answers**: Do not write answer paragraphs based on reasoning from the transcript alone without at least one actual search result. If searches found nothing, say so explicitly.
