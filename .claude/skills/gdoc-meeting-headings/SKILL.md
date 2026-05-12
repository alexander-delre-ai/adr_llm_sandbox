---
name: gdoc-meeting-headings
description: Reads meeting headings (titles) from a specified tab in a Google Document. Handles tab-based meeting logs where each meeting is a table row with its title in the first column. Tracks which meetings have already been processed in state.json.
---

# /gdoc-meeting-headings

Read and list all meeting headings from a named tab in a Google Document, and track which ones have already been processed.

## Input

Provide a Google Doc URL. The tab can be identified in three ways (checked in this order):

1. **Tab ID in URL**: `?tab=t.XXXXXXXX` query parameter (for example `https://docs.google.com/document/d/DOC_ID/edit?tab=t.ty5fqvxffq36`)
2. **Tab name in request**: User says "from the SDV SW tab" or "tab: Virtual Toolchain"
3. **No tab specified**: List available tabs and ask which one to use

## State file

Processing state is stored at `.claude/skills/gdoc-meeting-headings/state.json`. It tracks which headings have been seen and processed across runs.

**Schema:**

```json
{
  "documents": {
    "<documentId>": {
      "title": "Human-readable document title",
      "tabs": {
        "<tabId>": {
          "title": "Tab name",
          "lastScanned": "ISO 8601 timestamp",
          "meetings": {
            "<heading text verbatim>": {
              "status": "new | processed | skipped",
              "processedAt": "ISO 8601 timestamp or null",
              "notes": "optional free-text note"
            }
          }
        }
      }
    }
  }
}
```

**Status values:**
- `new`: heading found but not yet processed
- `processed`: meeting has been run through a workflow (meeting-plan, meeting-summary, etc.)
- `skipped`: intentionally excluded from processing

## Steps

### 1. Parse the URL

Extract:
- **Document ID**: the segment between `/d/` and the next `/` in the URL
- **Tab ID**: the `tab=t.XXXXXXXX` value from the query string, if present

Example URL: `https://docs.google.com/document/d/1Akz3sRL8dzgwh1MWbcEGlNVeSYirTAkypQ5Q-tgkskg/edit?tab=t.ty5fqvxffq36`
- Document ID: `1Akz3sRL8dzgwh1MWbcEGlNVeSYirTAkypQ5Q-tgkskg`
- Tab ID: `t.ty5fqvxffq36`

### 2. Resolve the tab

The `mcp__claude_ai_Google_Drive__*` tools do not support listing or filtering by tab. Handle as follows:

- If a **tab ID** was found in the URL or the user named a tab, record it for state tracking purposes only. Content reading fetches the full document.
- Tab-specific filtering is not supported -- note this to the user if they request a specific tab and the doc has multiple tabs.

### 3. Read the document

Call `mcp__claude_ai_Google_Drive__read_file_content` with:
- `fileId`: the extracted document ID

If the file is not found (the document is not in the user's accessible Google Drive), report the error and stop. The document must be owned by or shared into the authenticated Google Drive account.

If `read_file_content` returns insufficient structure for heading extraction, also call `mcp__claude_ai_Google_Drive__download_file_content` with:
- `fileId`: the extracted document ID
- `exportMimeType`: `"text/plain"`

Use the richer of the two outputs for heading extraction.

### 4. Extract meeting headings

The document uses one of two common structures. Check both and use whichever yields results:

**Structure A - Table-based meetings** (most common):
The markdown output renders table cells with a leading ` | `. The first column of each row is the meeting title. Extract all lines matching:

```
^ \| (.+)$
```

That is: start of line, space, pipe, space, then the heading text. The captured group is the title.

**Structure B - Heading-styled paragraphs**:
The markdown uses `#`, `##`, or `###` prefixes for Google Docs heading styles. Extract all lines matching:

```
^#{1,3} (.+)$
```

**Filter the results**:
- Remove template placeholders: `MEETING_TITLE`, `Meeting Title`, `[MEETING TITLE]`
- Remove blank or whitespace-only entries after trimming
- Remove entries that are only punctuation or separators (for example `---`, `___`)
- Deduplicate while preserving order

### 5. Update state.json

Read `.claude/skills/gdoc-meeting-headings/state.json` (create it if it does not exist with `{}`).

For the current document + tab:
- Set `documents.<documentId>.title` to the doc title from `mcp__claude_ai_Google_Drive__get_file_metadata` (call it with the fileId if title is needed), or the document ID if unavailable
- Set `documents.<documentId>.tabs.<tabId>.title` to the resolved tab name
- Set `documents.<documentId>.tabs.<tabId>.lastScanned` to the current ISO 8601 timestamp
- For each extracted heading:
  - If the heading does not yet exist in `meetings`, add it with `status: "new"` and `processedAt: null`
  - If it already exists, leave its status and processedAt unchanged (never downgrade from `processed` to `new`)

Write the updated state back to `state.json`.

### 6. Output

Return a numbered list grouped by status. Show the tab name and document title in the header.

Example:

```
Meeting headings in "SDV SW" tab ([Internal] Project Katana Activity):

New (not yet processed):
  1. SDV OH
  2. SDV Braking quick sync

Already processed:
  3. Brakes and Steering Weekly  (processed 2026-04-28)
  4. SDV Standup  (processed 2026-04-29)
```

If no headings are found, say so and describe what content was found instead.

## Marking a meeting as processed

When another skill (for example `/meeting-plan` or `/meeting-summary`) finishes processing a meeting that was found via this skill, update state.json:

```json
"<heading text>": {
  "status": "processed",
  "processedAt": "<ISO 8601 timestamp>"
}
```

Do this before reporting completion of the other skill.

## MCP tools used

This skill uses the **claude.ai Google Drive** integration (tool prefix `mcp__claude_ai_Google_Drive__`):

| Tool | Purpose |
|------|---------|
| `mcp__claude_ai_Google_Drive__read_file_content` | Read document content as natural language/markdown |
| `mcp__claude_ai_Google_Drive__download_file_content` | Export document as plain text (fallback for heading extraction) |
| `mcp__claude_ai_Google_Drive__get_file_metadata` | Get document title |
| `mcp__claude_ai_Google_Drive__search_files` | Find documents by title or content |

**Limitation:** Tab-specific reading is not supported. The full document is read and headings are extracted from all content. If the document is not accessible (not owned by or shared into the connected Google account), `read_file_content` returns "Item not found" -- the user must ensure the document is in their Drive.

## Notes

- This skill only reads and lists headings plus updates state. It does not summarize, create tickets, or send Slack messages.
- Tabs that are mostly empty (1 character) are placeholders. Skip them and note that to the user if targeted.
- To process a listed meeting, use `/meeting-summary` or `/meeting-plan` with the relevant section from the doc.
