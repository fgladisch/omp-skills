---
name: finishing-a-development-branch
description: Use when completed branch work is ready to merge locally, publish as a pull request, retain, or discard.
---

# Finishing a Development Branch

Validate the branch, present feasible outcomes with Oh My Pi's structured tools, and perform only the authorized integration or cleanup action.

## Establish state

1. Use `bash` to inspect the current branch, worktree, status, remotes, recent commits, and remote default branch.
2. Use `read` for repository instructions and `read pr://<number>` when an existing pull request is relevant.
3. Resolve the intended base branch from explicit context or the remote default. Use `ask` if it remains materially ambiguous.
4. Stop on detached HEAD, unexpected uncommitted changes, or identical feature and base branches. Report the recovery needed instead of guessing.
5. Run fresh validation proportional to the branch changes. Do not present a failing branch as ready.

## Present outcomes

Use one `ask` call containing only actions that are currently feasible:

- merge into the base branch locally;
- push and create a pull request;
- keep the branch and worktree unchanged;
- discard the branch work.

For merge or pull-request choices, include the base, remote, branch, title or merge mode, validation result, and preservation policy. Mark the safest complete outcome as recommended.

The selection authorizes only the named action. Discard is destructive: require a second `ask` confirmation showing the branch, commits, uncommitted files, and worktree that will be removed.

## Execute

### Merge locally

Update the base only when repository policy and worktree state make it safe. Merge without force, then validate the merged result. Preserve the feature branch unless deletion was explicitly selected.

### Push and create a pull request

Prefer OMP's `github` tool when enabled; otherwise use the repository's configured CLI through `bash`. Push without force, create the pull request with the approved title and summary, report its URL, and preserve the local branch/worktree unless cleanup was selected.

### Keep

Leave the branch and worktree unchanged. Report their names and paths.

### Discard

After explicit destructive confirmation, remove only the named worktree and feature branch. Never delete the base branch or unrelated uncommitted work.

Apply `verification-before-completion` to every claim about validation, merges, pushes, pull requests, or cleanup.
