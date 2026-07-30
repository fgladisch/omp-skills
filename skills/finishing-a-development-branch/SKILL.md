---
name: finishing-a-development-branch
description: Use when completed branch work is ready to merge locally, publish as a pull request, retain, or discard.
---

# Finishing a Development Branch

Validate the branch, present the feasible outcomes, and perform only the selected integration or cleanup action.

## Establish state

1. Inspect the current branch, worktree, status, remotes, and repository instructions.
2. Resolve the intended base branch from explicit context or the remote default. Ask if it remains ambiguous.
3. Stop on detached HEAD, unexpected uncommitted changes, or when the feature and base branch are the same. Report the recovery needed instead of guessing.
4. Run fresh validation proportional to the branch changes. If it fails, report the failures and do not present the branch as ready.

## Present outcomes

Use `user_select` for the actions that are actually available:

- merge into the base branch locally, preserving the feature branch unless deletion is explicitly included;
- push and create a pull request;
- keep the branch and worktree unchanged;
- discard the branch work.

The selection authorizes the named merge, push/PR, or keep action. Discard remains destructive and requires a second confirmation showing the branch, commits, uncommitted files, and worktree that will be removed.

## Execute

### Merge locally

Update the base branch only when doing so is safe under repository policy, merge without force, and run relevant validation on the merged result. Preserve the feature branch unless the selected outcome explicitly included deletion or the user confirms it separately.

### Push and create a pull request

Show the intended remote, branch, PR title, and summary before the selection. After authorization, push without force and create the PR. Report its URL and preserve the feature branch/worktree unless the user asks for cleanup.

### Keep

Leave the branch and worktree unchanged and report their names and paths.

### Discard

After explicit destructive confirmation, remove the worktree safely and delete only the named feature branch. Never delete the base branch or unrelated uncommitted work.

Apply `verification-before-completion` to claims about tests, merges, pushes, PR creation, or cleanup.
