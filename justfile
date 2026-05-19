# https://just.systems

# Print the latest published release tag for a GitHub repo.
# Usage: just gh-latest actions/checkout
gh-latest repo:
    @gh api repos/{{repo}}/releases/latest --jq .tag_name

# Regenerate README.md from the CI logs in vars/.
regen-readme:
    @python3 dev/gen_readme.py

# For every `uses:` in .github/workflows/, print the action, its current
# pin, and the latest released tag on GitHub. Helpful before committing
# workflow edits — see [[feedback-gha-latest-majors]].
check-action-versions:
    #!/usr/bin/env bash
    set -euo pipefail
    grep -rhE '^\s*-?\s*uses:' .github/workflows \
      | sed -E 's|.*uses:[[:space:]]+||' \
      | sort -u \
      | while read -r line; do
          action=${line%@*}
          pin=${line##*@}
          repo=$(echo "$action" | cut -d/ -f1-2)
          tag=$(gh api "repos/$repo/releases/latest" --jq .tag_name 2>/dev/null || echo "n/a")
          printf "%-40s pinned %-10s latest %s\n" "$action" "$pin" "$tag"
      done
