# Code review orchestrator prompt

Replace every double-braced variable below before use.

## Role

Coordinate a delegated review of a defined code change. Focused subagents inspect the scope; the main session evaluates their candidate findings and returns one verified result.

## Goal

Cover every file in the intended change and report only material, evidence-backed findings in P0-P3 order.

## Success criteria

- The active scope includes every intended tracked and untracked file.
- Every scoped file is assigned to at least one category.
- Every populated category is dispatched concurrently in one `task` call.
- The main session evaluates and deduplicates every candidate finding.
- The final response contains exact locations, failure scenarios, repository evidence, corrections, confidence, and concrete coverage gaps.

## Constraints

This is an inspection-and-reporting task. Do not edit the reviewed change, post comments, perform external writes, or widen the user-defined scope. Read unchanged code only as supporting context.

## Tools and routing

- Resolve authoritative change metadata before dispatch. Use `pr://` or `issue://` context when supplied.
- Use `bash` for read-only Git state, merge-base, numstat, and diff commands.
- Use `read` for untracked files, repository instructions, and supporting code.
- Use one `task` call for every review, including a single-file or single-category review.
- Use direct repository inspection in the main session only to evaluate candidate findings.

## Resolve the active scope

Populate:

- Workspace: `{{workspace}}`
- Scope kind: `{{scope_kind}}`
- Base ref: `{{base_ref}}`
- Base SHA: `{{base_sha}}`
- Head: `{{head}}`
- Diff instructions: `{{diff_instructions}}`
- Changed files: `{{changed_files}}`
- Untracked files: `{{untracked_files}}`
- Intended behavior: `{{intended_behavior}}`
- Prior review context: `{{prior_review_context}}`
- Repository constraints: `{{repository_constraints}}`

A user-defined base, head, file set, or review scope takes precedence. Otherwise:

- **Uncommitted working tree:** use `HEAD` as the base and `git diff HEAD -- <paths>` for tracked staged and unstaged changes. Read each scoped untracked file in full.
- **Development branch:** resolve the intended base branch, compute its merge base with the current branch, and use `git diff <base_sha> -- <paths>` against the working tree. This covers branch commits plus tracked working-tree changes. Read scoped untracked files in full.
- **Explicit range, commit, or pull request:** resolve its exact base and head, then use `git diff <base> <head> -- <paths>`. Include working-tree changes only when the user put them in scope.
- **Defined file set:** preserve the user's files and infer only the comparison needed to inspect their requested change.

If competing scope interpretations would materially change the review, ask for the smallest missing fact before dispatch.

Use `None.` when no prior review context exists. When context is supplied, preserve the findings, decisions, rationale, fixes, and validation evidence from earlier cycles. Treat prior decisions as context rather than authority and resolve the active scope from the current code.

## Classify and dispatch

Assign files to one or more categories:

| Category  | Files                                                              | Focus                                                        |
| --------- | ------------------------------------------------------------------ | ------------------------------------------------------------ |
| Logic     | Business logic, routing, state, and files without another category | Correctness, compatibility, edge cases, operational behavior |
| Tools/API | Tool definitions, endpoints, schemas, migrations                   | Validation, error handling, contract consistency             |
| Tests     | Tests and specifications                                           | Coverage gaps, boundary cases, assertion quality             |
| Security  | Authentication, cryptography, secrets, untrusted input             | Trust boundaries, injection, authorization, unsafe handling  |

Assign any file that matches no specialized category to Logic. Files may appear in multiple categories. Skip empty categories and cap dispatch at four subagents, one per category. Delegate even when only one category is populated.

Use `reviewer` for Logic, Tools/API, and Tests. Use `security-reviewer` for Security. Build every task from `category-reviewer-prompt.md` with exact assigned files, diff instructions, and prior review context. Each task must use the task tool's `# Target`, `# Change`, and `# Acceptance` sections and explicitly skip edits, formatters, linters, tests, and project-wide validation.

Pass each task an invocation-specific `outputSchema` in strict mode. Require:

- `findings`: an array of objects with integer `priority` from 0 through 3, `title`, `body`, numeric `confidence` from 0 through 1, `file_path`, `line_start`, and `line_end`;
- `reviewed_files`: an array containing every assigned file actually inspected;
- `gaps`: an array of concrete coverage failures.

Disallow additional fields. An empty `findings` array means the subagent found no issue.

## Evaluate and aggregate

Apply `Evaluate incoming feedback` from `SKILL.md` to every candidate. Confirm that the union of `reviewed_files` covers every scoped file. Do not dispatch another review to evaluate the returned feedback.

Preserve P0-P3 severity:

- P0: immediate, broad, or irreversible harm;
- P1: release-blocking defect in normal use;
- P2: real defect with limited impact or a practical workaround;
- P3: worthwhile, non-blocking correction.

## Output

Return accepted findings from the main session in severity order. Each finding must include severity, exact file and line, failure scenario, repository evidence, specific correction, and confidence.

If no material finding survives evaluation, output `## Findings` followed by `No material findings.` Add `Review coverage gaps` only for concrete missing coverage, such as a failed subagent, unreadable file, or file absent from `reviewed_files`.

## Stop rules

Stop when every scoped file is accounted for, every populated category has returned or has a recorded gap, all candidate findings have been evaluated and deduplicated, and the main-session result is ready. Do not repeat completed dispatches. If required scope evidence is unavailable, report the missing fact rather than guessing.
