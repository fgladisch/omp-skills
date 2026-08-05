---
name: finalizing-changes
description: Use when a coherent set of changes is complete and needs to be validated, committed, merged, published as a pull request, or retained, whether the changes are uncommitted or already on a branch.
---

# Finalizing Changes

Validate a completed increment, present only feasible dispositions, and perform the authorized action without assuming the work already lives on a feature branch.

## Establish state

1. Use `bash` to inspect the current branch, worktree, status, remotes, recent commits, and remote default branch.
2. Use `read` for repository instructions and `read pr://<number>` when an existing pull request is relevant.
3. Identify the intended change set and whether it is uncommitted, committed relative to a base branch, or both. Separate unrelated changes instead of including them.
4. Resolve the base branch only for merge or pull-request outcomes. If the intended changes are on the base branch, determine whether repository policy permits committing there or requires a topic branch.
5. Stop on detached HEAD, unexpected unrelated changes, or an ambiguous change set. Report the recovery needed instead of guessing.
6. Run fresh validation proportional to the intended changes. Do not present failing changes as ready.

## Present outcomes

Use one `ask` call containing only actions that are currently feasible:

- commit the intended changes on the current branch;
- merge a completed topic branch into the base branch locally;
- publish the intended changes as a pull request, creating a topic branch first when required;
- keep the changes, branch, and worktree unchanged.

For a commit choice, include the current branch, intended files, proposed message, and validation result. For merge or pull-request choices, include the base, remote, source branch or planned new branch, title or merge mode, validation result, and preservation policy. Mark the safest complete outcome as recommended.

The selection authorizes only the actions named in that option. Creating a pull request may include creating a topic branch, committing, and pushing only when those steps were shown in the selected option.

## Execute

### Commit in place

Offer this only when repository policy permits committing to the current branch. Apply `commit` to include only the intended changes, then report the commit and preserved working state.

### Merge locally

Offer this only when a completed topic branch differs from the base branch and has no intended uncommitted changes. Update the base only when repository policy and worktree state make it safe. Merge without force, validate the merged result, and preserve the topic branch and worktree.

### Push and create a pull request

Prefer OMP's `github` tool when enabled; otherwise use the repository's configured CLI through `bash`. If the intended changes are uncommitted, create a topic branch first when repository policy requires one, then apply `commit` to include only those changes. Push without force and preserve the local branch and worktree.

#### Compose the pull request

Follow the repository's pull request template and title convention when present. Otherwise, inspect the complete `base...HEAD` diff and commit range, then write a description that stands on its own. Do not use only the latest commit, paste the commit log, or make reviewers reconstruct the purpose from the diff. A pull request should have one coherent goal; stop and split independent changes before publishing.

Use a short, specific title that summarizes the primary change. When the repository has no title convention, write it as an imperative sentence. Avoid vague titles such as `Fix bug`, `Update code`, or `Phase 1`.

Keep **What** and **Why** as the required core of the body:

```markdown
## What

<Summarize the resulting behavior and coherent scope. Mention major implementation
decisions or boundaries only when they help reviewers understand the change.>

## Why

<State the problem or opportunity, its impact, and the intended outcome. Explain why
this approach was chosen, including relevant constraints or tradeoffs.>

## Verification

- `<command or scenario>` — <observed result>
```

- Describe outcomes and behavior under **What**, not a file inventory or line-by-line retelling of the diff. State intentional non-goals when the scope could be misunderstood.
- Put decision context that the code cannot preserve under **Why**. Links to issues, incidents, or design documents supplement this explanation; they do not replace it.
- Report only fresh, observed checks under **Verification**. Include reproduction and validation steps for bug fixes, and before/after evidence for user-visible visual changes.
- Add a **Risks** section when the change has breaking behavior, migrations, rollout requirements, feature flags, known shortcomings, or meaningful operational risk.
- Use an issue-closing keyword such as `Closes #123` only when the pull request targets the default branch and fully resolves that issue. Otherwise, use a plain reference.
- Remove placeholders and omit optional sections that do not apply.

Review the title and body against the final diff immediately before creation. Create the pull request with the approved title and body, then report its URL.

### Keep

Leave the intended changes, branch, and worktree unchanged. Report their state, names, and paths.

Apply `verification-before-completion` to every claim about validation, commits, merges, pushes, or pull requests.
