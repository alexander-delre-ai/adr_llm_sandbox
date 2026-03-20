---
description: Crafts a compelling feature request for reMarkable's Wishes & Ideas support portal and guides the user through submitting the static form.
---

# reMarkable Feature Request

Helps you write and submit a feature request to reMarkable at https://support.remarkable.com/s/contactsupport/wishes-and-ideas.

## Form Fields

| Field | Required | Type |
|-------|----------|------|
| Profession | No | Dropdown |
| What's this about? | No | Dropdown |
| Web Email | Yes | Text |
| Subject | Yes | Text |
| Description | Yes | Textarea |

## Workflow

### Step 1 - Collect details

If not already provided in the prompt, ask for the following:

| Field | Required | Notes |
|-------|----------|-------|
| Web Email | Yes | Email to associate with the submission |
| Subject | Yes | Short feature title, max 10 words |
| Feature description | Yes | What the feature does |
| Use case | Yes | The problem it solves for you |
| Profession | No | e.g. Student, Teacher, Engineer, Designer, Executive, Other |
| What's this about? | No | e.g. reMarkable Paper, reMarkable Paper Pro, reMarkable app |
| Current workaround | No | How you handle it today |
| Acceptance criteria | No | Specific expectations for the feature |

### Step 2 - Craft Subject and Description

**Subject**: Short, imperative phrase, max 10 words.
Example: `Add folder-level template assignment for notebooks`

**Description**: Use this structure:

```
**What I'm requesting:**
<1-2 sentences describing the feature>

**Why it would be valuable:**
<2-3 sentences on the use case and the problem it solves. Use first person - "I need this because..." is more persuasive than abstract justification>

**Current workaround:**
<What the user does today, or "None">

**Acceptance criteria:**
<Bullet points if provided, otherwise omit this section>
```

Keep total under 300 words. Plain language only.

### Step 3 - Present submission guide

Show the user:

1. Filled form values:
   - **Profession**: <value or "leave blank">
   - **What's this about?**: <value or "leave blank">
   - **Web Email**: <email>
   - **Subject**: <subject>
   - **Description**: (in a copyable code block)

2. Steps:
   - Open: https://support.remarkable.com/s/contactsupport/wishes-and-ideas
   - Fill in the form with the values above
   - Click **Submit**

### Step 4 - Open the URL

```bash
xdg-open "https://support.remarkable.com/s/contactsupport/wishes-and-ideas"
```

## Notes

- reMarkable reads all submissions but cannot respond individually
- Submit one feature per form for clarity
