---
description: Crafts a compelling feature request for reMarkable's Wishes & Ideas support portal and guides the user through submission via the Salesforce chat widget.
---

# reMarkable Feature Request

Helps you write and submit a feature request to reMarkable at https://support.remarkable.com/s/contactsupport/wishes-and-ideas.

The portal uses a Salesforce chat widget (no API), so this skill crafts your message and guides you through the submission steps.

## Workflow

### Step 1 - Collect details

If not already provided in the prompt, ask for the following (can ask all at once):

| Field | Required | Notes |
|-------|----------|-------|
| First name | Yes | For the chat prechat form |
| Email | Yes | For the chat prechat form |
| Last name | No | For the chat prechat form (optional) |
| Product | No | See product list below |
| Feature title | Yes | Short name, max 10 words |
| Feature description | Yes | What the feature does |
| Use case | Yes | The problem it solves for you |
| Current workaround | No | How you handle it today |
| Acceptance criteria | No | Specific expectations for the feature |

**Product options:**
- reMarkable Paper (2nd gen)
- reMarkable Paper Pro
- Both / All devices
- reMarkable app (mobile/desktop)

### Step 2 - Craft the message

Write a concise, compelling feature request using this template:

```
**Feature Request: <feature title>**

**Product:** <product>

**What I'm requesting:**
<1-2 sentences describing the feature>

**Why it would be valuable:**
<2-3 sentences on the use case and the problem it solves. Use first person - "I need this because..." is more persuasive than abstract justification>

**Current workaround:**
<What the user does today, or "None">

**Acceptance criteria:**
<Bullet points if provided, otherwise omit this section>
```

Keep the total under 300 words. Plain language only - no marketing speak.

### Step 3 - Present the submission guide

Show the user:

1. The crafted message in a copyable code block
2. Prechat field values to enter:
   - **First name**: <first name>
   - **Last name**: <last name>
   - **Email**: <email>
   - **Product**: <product>
   - **Category**: Wishes & Ideas (pre-selected via URL)
3. Steps:
   - Open: https://support.remarkable.com/s/contactsupport/wishes-and-ideas
   - Click the chat widget that appears on the page
   - Fill in the prechat form:
     - **First name** (required): <first name>
     - **Email** (required): <email>
     - **Last name** (optional): <last name if provided>
     - **Product** (optional): <product if provided>
     - **I have a question about**: Wishes & Ideas (pre-selected via URL)
   - Paste the message into the chat and send

### Step 4 - Open the URL

Run this command to open the page in the user's default browser:

```bash
xdg-open "https://support.remarkable.com/s/contactsupport/wishes-and-ideas"
```

## Notes

- The `wishes-and-ideas` URL path pre-routes the chat widget to the feature request flow
- Submit one feature per chat session for clarity
- reMarkable aggregates community requests - clear, specific requests have more impact
