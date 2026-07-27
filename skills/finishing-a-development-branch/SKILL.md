---
name: finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Validate branch context → verify tests → simplify when useful → present options → execute choice → clean up.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

## The Process

### Step 1: Validate Branch Context

Start with the `base_branch`, `feature_branch`, and `base_sha` recorded by the implementation workflow, then read the actual current branch:

```bash
current_branch=$(git branch --show-current)
```

Stop immediately if HEAD is detached.

For direct use without recorded context, resolve the missing values before validation. Determine the base branch from an explicit project convention or `refs/remotes/origin/HEAD`:

```bash
remote_default=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null || true)
base_branch=${remote_default#origin/}
feature_branch=$current_branch
```

If no remote default exists, use an unambiguous local `main` or `master`; ask the user if neither or both establish the intended base. Do not use `git merge-base` to infer a branch name because it returns a commit.

Once both names are known, verify that they are local branches and that the recorded feature branch is checked out:

```bash
git show-ref --verify --quiet "refs/heads/$base_branch"
git show-ref --verify --quiet "refs/heads/$feature_branch"
test "$current_branch" = "$feature_branch"
```

**Same-branch guard:** If `current_branch == base_branch`, the branch lifecycle precondition failed. Do not present merge, PR, keep-branch, or discard options. Report that implementation is already on the base branch and stop. Repairing commits already made on the base requires a separate, explicit recovery workflow.

For direct use, record the shared commit only after both branches and the same-branch guard are validated:

```bash
base_sha=$(git merge-base "$feature_branch" "$base_branch")
```

Finally, verify that `base_sha` identifies a commit in the feature branch's history:

```bash
git cat-file -e "${base_sha}^{commit}"
git merge-base --is-ancestor "$base_sha" "$feature_branch"
```

Stop if a branch is missing, the recorded feature branch is not checked out, or the recorded SHA is invalid or outside the feature branch's history.

### Step 2: Verify Tests

**Before presenting options, verify tests pass:**

```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**If tests fail:**

```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

Stop. Don't proceed to Step 3.

**If tests pass:** If the branch contains non-trivial code changes and simplify has not run for this diff, use **simplify** before presenting finish options. Skip for docs-only changes, tiny mechanical edits, or when an equivalent code-quality review already ran and found no issues. Then continue to Step 3.

### Step 3: Present Options

Use a single `user_select` call to present exactly these 4 options. Do not send a separate plain-text prompt before the tool call.

```json
{
  "question": "Implementation complete. What would you like to do?",
  "options": [
    { "label": "Merge back to <base-branch> locally" },
    { "label": "Push and create a Pull Request" },
    { "label": "Keep the branch as-is (I'll handle it later)" },
    { "label": "Discard this work" }
  ],
  "allowCustom": false
}
```

Map the selected label to the matching option in Step 4. If the selection is cancelled, leave the branch and worktree unchanged. **Don't add explanation** - keep the prompt and options concise.

### Step 4: Execute Choice

#### Option 1: Merge Locally

```bash
# Switch to base branch
git checkout <base-branch>

# Pull latest
git pull

# Merge feature branch
git merge <feature-branch>

# Verify tests on merged result
<test command>

# If tests pass
git branch -d <feature-branch>
```

Then: Cleanup worktree (Step 5)

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin <feature-branch>

# Create PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

Then: Cleanup worktree (Step 5)

#### Option 3: Keep As-Is

Report: "Keeping branch <name>. Worktree preserved at <path>."

**Don't cleanup worktree.**

#### Option 4: Discard

**Confirm first:**

```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:

```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Then: Cleanup worktree (Step 5)

### Step 5: Cleanup Worktree

**For Options 1, 2, 4:**

Check if in worktree:

```bash
git worktree list | grep $(git branch --show-current)
```

If yes:

```bash
git worktree remove <worktree-path>
```

**For Option 3:** Keep worktree.

## Quick Reference

| Option           | Merge | Push | Keep Worktree | Cleanup Branch |
| ---------------- | ----- | ---- | ------------- | -------------- |
| 1. Merge locally | ✓     | -    | -             | ✓              |
| 2. Create PR     | -     | ✓    | ✓             | -              |
| 3. Keep as-is    | -     | -    | ✓             | -              |
| 4. Discard       | -     | -    | -             | ✓ (force)      |

## Common Mistakes

**Skipping test verification**

- **Problem:** Merge broken code, create failing PR
- **Fix:** Always verify tests before offering options

**Open-ended questions**

- **Problem:** "What should I do next?" → ambiguous
- **Fix:** Present exactly 4 structured options

**Automatic worktree cleanup**

- **Problem:** Remove worktree when might need it (Option 2, 3)
- **Fix:** Only cleanup for Options 1 and 4

**No confirmation for discard**

- **Problem:** Accidentally delete work
- **Fix:** Require typed "discard" confirmation

## Red Flags

**Never:**

- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request

**Always:**

- Verify tests before offering options
- Present exactly 4 options
- Get typed confirmation for Option 4
- Clean up worktree for Options 1 & 4 only

## Integration

**Called by:**

- **subagent-driven-development** - After all tasks, simplify cleanup, the parallel formal review stage, accepted fixes, and full-plan verification; receives the recorded base branch, feature branch, and implementation-start SHA

**Related skills:**

- **simplify** - Use after tests pass and before presenting finish options when the branch contains non-trivial code changes.
- **verification-before-completion** - Terminal gate for this workflow. Before claiming tests pass, merge/PR/discard/cleanup is complete, or the branch is ready, run fresh verification and report evidence.
