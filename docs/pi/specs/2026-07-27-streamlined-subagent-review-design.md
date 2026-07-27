# Streamlined Subagent Review Design

## Problem

`subagent-driven-development` currently dispatches a spec-compliance reviewer and a code-quality reviewer after every implementation task. Findings trigger worker fixes followed by mandatory re-review loops. For plans with several tasks, this creates excessive reviewer traffic and can leave the workflow cycling in code-quality review.

## Goal

Use one bounded review stage after the whole implementation plan has landed. Preserve independent spec and quality perspectives by running two narrowly scoped reviewers in parallel. Do not automatically re-run reviewers after fixes.

## Non-goals

- Removing worker self-review, task tests, or escalation behavior.
- Combining spec and code-quality concerns into one reviewer prompt.
- Removing the `simplify` cleanup workflow.
- Parallelizing implementation writes in the active worktree.
- Preventing a user or controller from explicitly requesting an additional review when risk warrants it.

## Workflow

1. Read the implementation plan, extract all tasks, and record the branch base SHA.
2. Dispatch one fresh worker per task, sequentially against the active worktree.
3. Each worker implements, tests, commits, self-reviews, and reports status. No reviewer is dispatched between tasks.
4. Stop immediately when a worker is blocked, needs context, reports correctness concerns, or fails required verification. Resolve that condition before continuing.
5. After every plan task is implemented, run `simplify` once with the explicit comparison range `<plan-base-sha>..HEAD`. Apply accepted cleanup findings, verify them, and commit any cleanup changes.
6. Capture the shared review head SHA after the cleanup commit. Run one formal review stage by dispatching two fresh, read-only reviewers in parallel:
   - The final reviewer checks whole-plan spec compliance and cross-task integration.
   - The code-quality reviewer checks implementation quality across the full branch diff.
7. Aggregate and deduplicate both reports. Critical and Important findings block completion. Minor findings are advisory.
8. If blocking findings exist, dispatch one fresh fixer worker with the complete accepted findings list. The fixer applies the fixes, runs the plan verification commands, and commits once.
9. Do not automatically dispatch either reviewer again. Run fresh full-plan verification and inspect the final diff before handing off to `finishing-a-development-branch`.

The two parallel reviewers form one review stage. `simplify` remains a separate cleanup pass before formal review.

## Reviewer Responsibilities

### Final reviewer

`final-reviewer-prompt.md` owns:

- Line-by-line compliance with the complete implementation plan.
- Missing, extra, or misunderstood requirements.
- Acceptance criteria spanning multiple tasks.
- Cross-task integration and consistency.
- Evidence that the implemented branch behaves as one coherent result.

It does not assess naming, style, decomposition, performance, or general maintainability unless those are explicit plan requirements.

### Code-quality reviewer

`code-quality-reviewer-prompt.md` owns:

- Correctness risks that are visible in implementation details.
- Test quality and meaningful behavioral coverage.
- Maintainability, naming, decomposition, and consistency with project patterns.
- Security, error handling, concurrency, and performance concerns.
- Dead code and boundary leaks introduced by the complete branch diff.

It does not perform a line-by-line plan-compliance audit.

Both reviewers inspect the same base-to-head branch range after `simplify`. Both are read-only and return evidence-backed findings with file and line references.

## Finding Handling

The controller combines both reports into a single disposition:

- **Critical:** must be fixed before handoff.
- **Important:** must be fixed before handoff.
- **Minor:** advisory and non-blocking. Leave it deferred when there are no blocking findings. If a fixer worker is already required, include a Minor finding only when it is cheap, clearly within scope, and safe to combine with the blocking fixes.
- **Rejected:** false positive, duplicate, outside approved scope, or contradicted by repository evidence.

One fixer worker receives all accepted blocking findings and any accepted Minor findings so it can account for interactions between tasks. The fixer does not broaden product scope or make unapproved architectural decisions. Such decisions return to the user.

There is no automatic reviewer approval loop after the fixer. Final confidence comes from fresh full-plan verification plus parent inspection of the resulting diff. An additional focused review is an explicit exception chosen by the user or controller for a concrete risk.

## File Changes

### `skills/subagent-driven-development/SKILL.md`

- Replace the per-task two-stage review principle with one post-plan parallel review stage.
- Remove per-task spec and quality dispatches and their re-review loops from the process diagram, dispatch instructions, examples, advantages, costs, and red flags.
- Keep worker self-review, task verification, status handling, and sequential write safety.
- Move `simplify` before formal branch review, pass the plan's base-to-head range, and commit cleanup changes before capturing the review head SHA.
- Document parallel reviewer dispatch, finding synthesis, one fixer worker, and the no-automatic-re-review rule.

### `skills/simplify/SKILL.md`

Allow a caller to supply an explicit git comparison range. Preserve the existing working-tree diff behavior when no range is supplied. This lets plan workflows review all committed implementation changes rather than an empty working tree.

### `skills/subagent-driven-development/final-reviewer-prompt.md`

Add a whole-plan spec-compliance and integration prompt. It receives the full plan path, base SHA, head SHA, working directory, branch, implementation summary, and verification commands.

### `skills/subagent-driven-development/code-quality-reviewer-prompt.md`

Retain this file and adapt it from per-task review to full-branch review. Keep its scope distinct from final plan compliance.

### `skills/subagent-driven-development/spec-reviewer-prompt.md`

Remove this obsolete per-task prompt. Its necessary whole-plan responsibilities move into `final-reviewer-prompt.md`.

### `skills/requesting-code-review/SKILL.md`

Change the subagent-driven-development integration from mandatory review after each task to one parallel review stage after the complete plan. Keep its guidance for ad-hoc development and major features.

### `README.md`

No table change is required because the skill's invocation trigger and frontmatter description remain unchanged. The skill directory and README row must still be checked for repository sync before completion.

## Verification

Before completion:

1. Search the affected skills for stale requirements to review after each task, run spec review before quality review, or loop until reviewer approval.
2. Confirm every prompt filename referenced by `subagent-driven-development/SKILL.md` exists and the removed prompt is unreferenced.
3. Confirm the process diagram and example show `simplify` reviewing the explicit plan base-to-head range before the parallel final review stage.
4. Confirm cleanup changes are verified and committed before the shared review head SHA is captured.
5. Confirm both reviewer prompts use the complete plan and shared branch base-to-head range while preserving separate scopes.
6. Confirm only one automatic fixer worker is described and no automatic reviewer rerun follows it.
7. Run the repository's available formatting or validation checks.
8. Verify the README skill table remains in one-to-one sync with `skills/` directories and frontmatter descriptions.

## Risks and Mitigations

- **Defects compound across tasks before review:** workers retain self-review, task-level tests, and escalation gates. Full-plan review adds cross-task visibility that per-task reviewers lacked.
- **Parallel reviewers duplicate findings:** the controller explicitly aggregates and deduplicates reports before dispatching the fixer.
- **Fixes introduce new defects without re-review:** the fixer must run complete plan verification, and the parent inspects the final diff. Additional review remains available as an explicit risk-based exception.
- **`simplify` changes behavior before review:** cleanup is verified and committed before the shared review head SHA is captured, so both reviewers inspect it.
- **Large final diffs increase reviewer load:** prompts give each reviewer a limited scope and the full base-to-head range. Plans that exceed a practical review context should be split before implementation rather than restoring per-task approval loops.
