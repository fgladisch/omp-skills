---
name: test-driven-development
description: Use for behavior changes and bug fixes when an automated test or executable regression check can establish the expected result before production code changes.
---

# Test-Driven Development

Use a failing executable check to define observable behavior, then make the smallest change that satisfies it.

## Red

1. Choose one externally meaningful behavior, boundary, invariant, transition, or regression.
2. Find the repository's test conventions with `glob`, `grep`, and targeted `read` calls.
3. Add the smallest test that expresses the expected public behavior.
4. Run the focused check with `bash` and confirm it fails for the intended reason. Syntax errors, missing dependencies, and unrelated failures do not establish red.

For a service needed by the check, start and supervise it with `hub`, not a detached shell command. For browser-visible behavior, use `browser` to establish the failing interaction when an automated test is not the right contract.

## Green

1. Make the smallest sufficient production change with `edit`.
2. Use `lsp` for definitions, references, renames, imports, and code actions; do not hand-edit a cross-file symbol change.
3. Run the focused check until it passes.
4. Run broader checks proportional to regression risk.
5. Smoke-test the changed path through the real entry point.

## Refactor

Refactor only while checks remain green. Use `ast_edit` for structural codemods that would be unsafe as text replacement, and apply the staged rewrite only after reviewing its proposal.

Tests must be deterministic, isolated, and resistant to implementation-only changes. Prefer real collaborators when cheap and reliable; use fakes or mocks only at slow, unstable, destructive, or external boundaries. Do not add production APIs solely for tests.

## Review

After the Green and Refactor steps, apply `code-review` when the change carries meaningful compatibility, security, data-integrity, or operational risk. Keep review optional for small, low-risk changes.

## Practical exceptions

Strict test-first may add little value for documentation, generated artifacts, configuration-only edits, exploratory spikes, UI-only visual changes, or environments without a usable harness. Proceed without asking when the exception is clear and record the executable, browser, or artifact validation used instead. For hard-to-isolate legacy code, add the narrowest characterization or integration check that exposes the regression.

Do not delete correct pre-existing work because its tests were written later. Improve its evidence from the current state. Apply `verification-before-completion` before claiming the behavior works or the regression is covered.
