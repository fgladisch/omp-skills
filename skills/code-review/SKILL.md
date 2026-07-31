---
name: code-review
description: Use when reviewing a change, evaluating code-review feedback, or cleaning up a scoped diff before completion or integration.
---

# Code Review

Find material defects in a defined change, evaluate them against repository evidence, and fix accepted findings when the request authorizes edits.

## Load the review scope

Use Oh My Pi's structured surfaces before reconstructing context manually:

- `read pr://<number>` or `read issue://<number>` for GitHub context;
- `bash` for focused Git commands such as `git status --short`, `git diff`, and `git show`;
- `read` for exact file sections, `glob` for paths, and `grep` for textual evidence;
- `lsp` for definitions, implementations, diagnostics, and references. Run references before changing an exported symbol.

Determine the intended behavior, repository conventions, exact diff or feedback items, and whether the request is review-only or authorizes fixes. If scope cannot be inferred from the repository or request, use `ask` before reviewing the wrong change.

## Review the change

Prioritize defects affecting correctness, security, data integrity, compatibility, performance, and maintainability. Check for missing requirements, regressions, unhandled boundaries, duplicated behavior, unnecessary complexity, and tests that do not defend the changed contract.

Report findings in severity order:

- **P0** — immediate, broad, or irreversible harm;
- **P1** — release-blocking defect in normal use;
- **P2** — real defect with limited impact or a practical workaround;
- **P3** — worthwhile but non-blocking correction.

Each finding must include the exact file and location, failure scenario, repository evidence, specific correction, and confidence. Do not inflate style preferences into defects. If no material finding exists, say so and identify any validation gap.

## Use OMP reviewers when they add coverage

Review directly by default. For a broad or high-risk diff with genuinely independent angles, batch `task` calls using the `reviewer` and, when appropriate, `security-reviewer` agents. Give each agent the same explicit scope and a distinct review angle. Do not run reviewers serially.

Treat agent reports as leads, not verdicts. Validate every proposed finding against the current files and synthesize one deduplicated result.

## Evaluate incoming feedback

For each comment:

1. Verify the technical claim against current code, requirements, and supported environments.
2. Accept, reject, or request clarification with evidence.
3. Check whether the proposed correction expands scope or adds unused behavior.
4. Implement accepted findings only when edits are authorized.

Use `edit` for surgical changes, `lsp` for symbol-aware refactors and code actions, and `ast_edit` for structural codemods. Push back directly on incorrect or out-of-scope advice.

## Validate

Run the smallest check that exercises each accepted fix, then broader validation proportional to regression risk. For UI changes, drive the changed path with `browser`. Apply `verification-before-completion` before claiming the review or fixes are complete.
