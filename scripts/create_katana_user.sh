#!/usr/bin/env bash
set -euo pipefail

# ── Configuration ────────────────────────────────────────────────────────────
ACCOUNT_ID="055333015386"
KATANA_GROUP="katana"   # update if the actual IAM group name differs
# ─────────────────────────────────────────────────────────────────────────────

usage() {
  echo "Usage: $0 <username>"
  echo ""
  echo "Creates an IAM user in account ${ACCOUNT_ID} and adds them to the '${KATANA_GROUP}' group."
  exit 1
}

if [[ $# -ne 1 ]]; then
  usage
fi

USERNAME="$1"

# Validate aws CLI is available
if ! command -v aws &>/dev/null; then
  echo "ERROR: aws CLI not found. Install it from https://aws.amazon.com/cli/" >&2
  exit 1
fi

# Verify the active credentials target the expected account
ACTIVE_ACCOUNT=$(aws sts get-caller-identity --query Account --output text 2>/dev/null || true)
if [[ -z "$ACTIVE_ACCOUNT" ]]; then
  echo "ERROR: Unable to retrieve caller identity. Check your AWS credentials." >&2
  exit 1
fi

if [[ "$ACTIVE_ACCOUNT" != "$ACCOUNT_ID" ]]; then
  echo "ERROR: Credentials are for account ${ACTIVE_ACCOUNT}, expected ${ACCOUNT_ID}." >&2
  exit 1
fi

echo "Account verified: ${ACCOUNT_ID}"
echo "Creating IAM user: ${USERNAME}"

# Create the user (idempotent: skip if already exists)
if aws iam create-user --user-name "${USERNAME}" 2>&1 | grep -q "EntityAlreadyExists"; then
  echo "WARNING: User '${USERNAME}' already exists, skipping creation."
else
  echo "User '${USERNAME}' created."
fi

# Add user to the katana group
echo "Adding '${USERNAME}' to group '${KATANA_GROUP}'..."
aws iam add-user-to-group --group-name "${KATANA_GROUP}" --user-name "${USERNAME}"
echo "Group membership added."

# Confirm
echo ""
echo "Groups for '${USERNAME}':"
aws iam list-groups-for-user --user-name "${USERNAME}" \
  --query 'Groups[].GroupName' --output table

echo ""
echo "Done. User '${USERNAME}' is now a member of '${KATANA_GROUP}'."
