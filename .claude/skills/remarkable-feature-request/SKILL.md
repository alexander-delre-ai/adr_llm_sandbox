---
name: remarkable-feature-request
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

**Defaults (use unless the user overrides):**

| Field | Default |
|-------|---------|
| Profession | Engineering |
| What's this about? | New Functionality |
| Web Email | alexanderdelre@gmail.com |

If the user described the feature request in their prompt, infer Subject and Description from it directly - do not re-ask for what was already provided. Only prompt for Subject or Description if the request contains no usable content.

Optional fields (current workaround, acceptance criteria) - include only if the user mentioned them.

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
