#!/usr/bin/env bash
set -euo pipefail

# Purge all deployments in a repository without deleting environments.
# Requires:
#  - REPO="owner/repo"
#  - TOKEN="GitHub token" (in Actions: GITHUB_TOKEN is provided)
#
# The script:
# 1) Lists all deployments (paginated, 100 per page)
# 2) Sets each deployment status to inactive
# 3) Deletes the deployment
# 4) Prints a summary per environment and total

REPO="${REPO:-${GITHUB_REPOSITORY:-}}"
TOKEN="${TOKEN:-${GITHUB_TOKEN:-}}"

if [[ -z "${REPO}" ]]; then
  echo "ERROR: REPO is not set (expected owner/repo)."
  exit 1
fi
if [[ -z "${TOKEN}" ]]; then
  echo "ERROR: TOKEN/GITHUB_TOKEN is not set."
  exit 1
fi

# Ensure jq is available
if ! command -v jq >/dev/null 2>&1; then
  echo "jq is not installed. Attempting to install..."
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update -y
    sudo apt-get install -y jq
  else
    echo "ERROR: jq is required but could not be installed automatically."
    exit 1
  fi
fi

api() {
  local method="$1"
  local path="$2"
  local data="${3:-}"
  if [[ -n "$data" ]]; then
    curl -sS -X "$method" \
      -H "Authorization: Bearer ${TOKEN}" \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      -H "Content-Type: application/json" \
      --data "$data" \
      "https://api.github.com${path}"
  else
    curl -sS -X "$method" \
      -H "Authorization: Bearer ${TOKEN}" \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      "https://api.github.com${path}"
  fi
}

echo "Listing deployments for ${REPO} ..."
declare -a IDS=()
declare -a ENVS=()

page=1
while true; do
  resp="$(api GET "/repos/${REPO}/deployments?per_page=100&page=${page}")"
  count="$(echo "$resp" | jq 'length')"
  if [[ "$count" -eq 0 ]]; then
    break
  fi
  # Collect id and environment for each deployment
  while IFS=$'\t' read -r id env; do
    IDS+=("$id")
    ENVS+=("$env")
  done < <(echo "$resp" | jq -r '.[] | "\(.id)\t\(.environment // "unknown")"')
  ((page++))
done

if [[ "${#IDS[@]}" -eq 0 ]]; then
  echo "No deployments found. Nothing to delete."
  exit 0
fi

echo "Found ${#IDS[@]} deployments. Deactivating and deleting..."
declare -A COUNTS
total=0

for i in "${!IDS[@]}"; do
  id="${IDS[$i]}"
  env="${ENVS[$i]}"
  # Mark as inactive (safe precondition for deletion)
  api POST "/repos/${REPO}/deployments/${id}/statuses" '{"state":"inactive"}' >/dev/null || true
  # Delete deployment
  api DELETE "/repos/${REPO}/deployments/${id}" >/dev/null || true
  COUNTS["$env"]=$(( ${COUNTS["$env"]:-0} + 1 ))
  total=$((total + 1))
done

echo "Deleted deployments summary:"
for k in "${!COUNTS[@]}"; do
  printf "  %s: %d\n" "$k" "${COUNTS[$k]}"
done
printf "Total: %d\n" "$total"