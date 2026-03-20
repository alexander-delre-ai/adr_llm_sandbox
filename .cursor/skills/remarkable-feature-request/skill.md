# reMarkable Feature Request

Crafts and submits a feature request to reMarkable's "Wishes & Ideas" support portal.

## Submission URL

https://support.remarkable.com/s/contactsupport/wishes-and-ideas

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

If not already provided, prompt the user for:

| Field | Required | Notes |
|-------|----------|-------|
| Web Email | Yes | The email to associate with the submission |
| Subject | Yes | Short feature title, max 10 words |
| Feature description | Yes | What the feature does and why it's valuable |
| Use case | Yes | The specific problem it solves |
| Profession | No | e.g. Student, Teacher, Engineer, Designer, Executive, Other |
| What's this about? | No | e.g. reMarkable Paper, reMarkable Paper Pro, reMarkable app |
| Current workaround | No | How they handle it today |
| Acceptance criteria | No | Specific expectations for how it should work |

### Step 2 - Craft the Subject and Description

**Subject** (maps to the Subject field): Short, imperative, max 10 words.
Example: `Add folder-level template assignment for notebooks`

**Description** (maps to the Description textarea): Use this structure:

```
**What I'm requesting:**
<1-2 sentences describing the feature clearly>

**Why it would be valuable:**
<2-3 sentences on the use case and problem it solves. Use first person - "I need this because..." lands better than abstract justification>

**Current workaround:**
<What the user does today, or "None">

**Acceptance criteria:**
<Bullet points if provided, otherwise omit this section>
```

Keep the total description under 300 words. Plain language only - no marketing speak.

### Step 3 - Present submission instructions

Display:

1. The filled form values in a clear summary:
   - **Profession**: <value or "leave blank">
   - **What's this about?**: <value or "leave blank">
   - **Web Email**: <email>
   - **Subject**: <subject>
   - **Description**: (copyable code block with the crafted description)

2. Steps:
   - Open: https://support.remarkable.com/s/contactsupport/wishes-and-ideas
   - Fill in the form fields with the values above
   - Click **Submit**

### Step 4 - Open the URL

```bash
xdg-open "https://support.remarkable.com/s/contactsupport/wishes-and-ideas"
```

## Notes

- reMarkable reads all submissions but cannot respond to each individually
- Submit one feature per form submission for clarity
- The "Wishes & Ideas" path pre-selects the correct category
