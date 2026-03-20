# reMarkable Feature Request

Crafts and submits a feature request to reMarkable's "Wishes & Ideas" support portal. Since the portal uses a Salesforce chat widget, this skill generates a polished feature request message and guides the user through submission.

## Submission URL

https://support.remarkable.com/s/contactsupport/wishes-and-ideas

## Workflow

### Step 1 - Collect user info

If not already provided, prompt the user for:

| Field | Required | Purpose |
|-------|----------|---------|
| First name | Yes | Prechat field (required by chat widget) |
| Email | Yes | Prechat field (required by chat widget) |
| Last name | No | Prechat field (optional) |
| Product | No | Which reMarkable product this applies to |
| Feature title | Yes | Short, clear name for the feature (max 10 words) |
| Feature description | Yes | What the feature does |
| Use case | Yes | Why the user needs it; what problem it solves |
| Workaround | No | How they currently handle it (if any) |

**Products to offer:**
- reMarkable Paper (2nd gen)
- reMarkable Paper Pro
- Both / All devices
- reMarkable app (mobile/desktop)

### Step 2 - Craft the feature request

Write a concise, compelling feature request message using this structure:

```
**Feature Request: <feature title>**

**Product:** <product>

**What I'm requesting:**
<1-2 sentences describing the feature clearly>

**Why it would be valuable:**
<2-3 sentences on the use case and problem it solves. Be specific and personal - "I need this because..." lands better than abstract justification>

**Current workaround:**
<What the user does today, or "None" if there's no workaround>

**Acceptance criteria (optional):**
<If the user has specific expectations for how the feature should work, list them here as bullet points>
```

Keep the total message under 300 words. Use plain language, not marketing speak.

### Step 3 - Present submission instructions

Display the following to the user:

1. The crafted feature request message (in a copyable code block)
2. Step-by-step submission guide:
   - Open: https://support.remarkable.com/s/contactsupport/wishes-and-ideas
   - Click **"Chat with us"** or the chat widget that appears
   - Fill in the prechat form:
     - **First name** (required): <first name>
     - **Email** (required): <email>
     - **Last name** (optional): <last name if provided>
     - **Product** (optional): <product if provided>
     - **I have a question about**: Wishes & Ideas (pre-selected via URL)
   - Paste the crafted message into the chat
   - Send and follow any prompts from the support agent

### Step 4 - Open the URL

Run the following shell command to open the page in the user's default browser:

```bash
xdg-open "https://support.remarkable.com/s/contactsupport/wishes-and-ideas"
```

## Notes

- The "wishes-and-ideas" URL path pre-routes the chat to the feature request flow
- The portal uses Salesforce Embedded Messaging - there is no API or form POST endpoint to automate
- Multiple feature requests should be submitted as separate chat sessions
- reMarkable does not guarantee responses to feature requests, but they aggregate community votes
