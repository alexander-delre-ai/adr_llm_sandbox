---
description: Searches Slack, Confluence, JIRA, and the codebase to answer questions arising from meetings. Takes a question and optional meeting context, runs multi-source searches, and synthesizes findings into a structured response with sources. Use when researching unresolved questions, looking up prior decisions, or finding implementation details related to meeting discussions.
---

# Meeting Research

Searches Slack, Confluence (Applied + KATA), JIRA (AVP + KATA), and optionally the local codebase to find answers to questions from meeting discussions. Produces a structured response with synthesized answer, sources, and identified gaps.

**MCP naming**: Use whichever Atlassian and Slack MCP tools your session exposes. This document uses illustrative server names (`user-Slack`, `user-atlassian-mcp-applied`, `user-atlassian-mcp-kata`); in Claude Code, these often appear as `mcp__kata-atlassian__*`, `mcp__claude_ai_Slack__*`, etc. Prefer the tools listed in `CLAUDE.md` at the repository root when names differ.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| question | Yes | The specific question to research |
| context | No | Meeting workspace path (e.g., `workspaces/2026-03-13/sdv-sw-oh`) or inline background context |
| scope | No | Comma-separated source list: `slack`, `confluence`, `jira`, `codebase`. Defaults to all. |

## Workflow

### Step 1: Parse question and generate search terms

- Extract key technical terms and entities from the question
- If a workspace path is provided, read `analysis.md` and `transcript.md` or `summary.md` for background
- Generate 2-4 keyword search variants:
  - **Broad**: core nouns and verbs (e.g., "current draw HSD efuse")
  - **Narrow**: exact phrases or specific terms (e.g., "current readback HSD application")
  - **Synonym**: alternate terminology (e.g., "efuse current feedback software")

### Step 2: Search Slack

Use your configured Slack MCP.

- Run 2-3 parallel searches using `slack_search_public_and_private`:
  - `query: "<keyword variant>"`
  - `sort: "timestamp"`
  - `sort_dir: "desc"`
  - `include_context: true`
  - `limit: 10`
- For promising thread results, follow up with `slack_read_thread` to get full context
- Deduplicate results across query variants by `message_ts`

### Step 3: Search Confluence (Applied first, then KATA)

Search Applied spaces first: platform firmware team documents drivers, roadmaps, design docs, and implementation details here.

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

### Step 4: Search JIRA (Applied first, then KATA)

Search Applied JIRA first: AVP tickets contain implementation-level detail on firmware drivers, platform roadmap items, etc.

**Applied JIRA (AVP)** (cloudId: `6461690f-d275-4167-8055-cc3dc06e03f2`):

- `searchJiraIssuesUsingJql` with JQL such as: `text ~ "term1" AND text ~ "term2" ORDER BY created DESC`
- `maxResults: 10`
- Request fields such as summary, description, status, priority, assignee
- Use markdown response format when supported

**KATA JIRA** (cloudId: `eadd00c6-0d3f-4c89-99e3-ad95a0daaa51`):

- Same approach on the KATA project

### Step 5: Search codebase (conditional)

**Codebase location** (default): `~/applied/core-stack` or the path in your environment for the Vehicle OS / core-stack checkout.

Only triggered if the question involves implementation, architecture, API design, or code-level details. Trigger heuristic: question contains terms like: "implement", "code", "API", "function", "driver", "system.py", "module", "PR", "merge", "design pattern", or references specific architecture components.

- Semantic search with `target_directories` set to that repo for broad questions
- `Grep` with `path` set to that repo for symbol or function lookups
- `Glob` with `target_directory` set to that repo for file patterns

### Step 6: Synthesize and present findings

- Provide a **consolidated answer** at the top that directly addresses the question
- Group supporting findings by source (Slack, Confluence, JIRA, Codebase)
- For each finding: short summary, direct link or permalink, date, and relevance note
- Flag contradictions or gaps across sources
- Suggest follow-up actions if the question remains unresolved

## Output Format

### Standalone usage (single question)

```markdown
## Research: <question summary>

### Answer
<Direct synthesized answer citing sources>

### Slack
- **<channel or DM name>** (<date>): <summary> [link]
  - Relevance: <why this matters>

### Confluence
- **<page title>** (<space>, <last modified>): <summary> [link]
  - Relevance: <why this matters>

### JIRA
- **<TICKET-KEY>**: <summary>, Status: <status> [link]
  - Relevance: <why this matters>

### Codebase (if applicable)
- **<file path>**: <what was found>
  - Relevance: <why this matters>

### Gaps / Follow-up
- <unresolved aspects or suggested next steps>
```

### Batch usage (meeting_plan integration)

When called from `meeting_plan` against multiple unresolved questions, compile results into a single `research.md`:

```markdown
# Research: <Meeting Title> (<Date>)

Generated from unresolved questions in analysis.md, Section 4.

---

## Q1: <question text>
[Owner: <person>]

### Answer
<synthesized answer>

### Sources
- **Slack**: <findings with links>
- **Confluence**: <findings with links>
- **JIRA**: <findings with links>
- **Codebase**: <findings if applicable>

### Gaps
- <unresolved aspects>

---

## Q2: <next question>
[repeat structure]
```

Omit empty source sections. If a question yields no results from any source, state "No relevant results found" and suggest alternative search strategies.

## Rules

- **Parallel searches**: Run Slack, Confluence, and JIRA searches in parallel where possible to minimize latency
- **Applied first**: Always search Applied or AVP spaces before KATA spaces in Confluence and JIRA when both apply
- **Deduplication**: Same content found via multiple queries should appear only once
- **Source links**: Always include permalinks or URLs so the user can verify findings
- **Relevance filtering**: Exclude results that mention search terms but are clearly unrelated to the question context
- **Large results**: If a Confluence page is relevant, fetch full content with `getConfluencePage` rather than relying on search excerpts only
- **Codebase gating**: Only search the codebase when the question is clearly about implementation or architecture; skip for process, scheduling, or coordination questions
