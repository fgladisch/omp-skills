---
name: commit
description: Use when the user asks to commit, create a commit, stage and commit, or run git commit; follows repository conventions with gitmoji as the fallback.
---

# Commit

Create one intentional commit from an evidence-backed file set and message.

## Prepare

1. Use `read` for repository commit instructions and `bash` for recent commit subjects.
2. Inspect `git status --short`, `git diff`, and `git diff --cached`.
3. Stop if there are no changes. Preserve unrelated user changes and split unrelated concerns.
4. Run validation proportional to the selected files unless the user explicitly requested a no-verify workflow.

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

## Resolve ambiguity

The user's commit request authorizes committing the intended change, not unrelated files, hook bypasses, amendments, or pushes. Infer the file set and message from the completed task and repository conventions.

Use OMP's `ask` tool only when materially different file groupings or messages remain plausible. Show the proposed message, exact file list, and validation result together; offer concrete choices and mark the safest complete choice as recommended.

## Commit

Stage specific paths with `bash`. Do not use `git add .` or `git add -A` unless the whole working tree is explicitly in scope. Create the commit without interactive flags, then inspect the new commit and `git status --short`.

If a hook fails, report the complete failure and leave the commit uncreated. Fix hook failures only when the original request authorizes those edits. Never bypass hooks, amend, push, add attribution, or broaden the file set without explicit authorization.

Apply `verification-before-completion` before reporting the commit created.
