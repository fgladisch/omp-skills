---
name: commit
description: Use when the user asks to commit, create a commit, stage and commit, or run git commit; follows repository conventions with gitmoji as the fallback.
---

# Commit

Create one intentional commit from an explicitly confirmed file set and message.

## Prepare

1. Read project commit instructions and recent commit subjects.
2. Inspect `git status --short`, `git diff`, and `git diff --cached`.
3. Stop if there are no changes. Separate unrelated concerns rather than hiding them in one commit.
4. Run validation proportional to the selected changes unless the user explicitly requested a no-verify workflow.

Follow the repository's commit format. If none exists, use `<gitmoji> <type>: <description>` with a concise subject:

| Change                 | Fallback       |
| ---------------------- | -------------- |
| Feature                | `✨ feat:`     |
| Fix                    | `🐛 fix:`      |
| Refactor               | `♻️ refactor:` |
| Tests                  | `✅ test:`     |
| Documentation          | `📝 docs:`     |
| Removal                | `🔥 remove:`   |
| Tooling or maintenance | `🔧 chore:`    |

## Confirm

Use `user_select` once to show the proposed message, exact file list, and validation result. Offer: commit as-is, edit message, edit files, or cancel. Reconfirm after edits.

## Commit

Stage specific paths. Do not use `git add .` or `git add -A` unless the user explicitly selected the whole working tree. Create the commit without interactive flags, then inspect `git status --short` and the new commit.

If a hook fails, report the failure and keep the commit uncreated. Fix hook failures only when authorized by the original request or a follow-up. Never bypass hooks, amend, push, add attribution, or broaden the file set without explicit authorization.
