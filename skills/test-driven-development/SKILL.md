---
name: test-driven-development
description: Use for behavior changes and bug fixes when an automated test or executable regression check can establish the expected result before production code changes.
---

# Test-Driven Development

Use a failing check to define observable behavior, then make the smallest change that satisfies it.

## Red, green, refactor

1. Choose one externally meaningful behavior or regression.
2. Write the smallest test that expresses the expected result using public behavior where practical.
3. Run it and confirm it fails for the intended reason. A syntax error or unrelated failure does not establish the red state.
4. Implement the smallest sufficient production change.
5. Run the focused test until it passes, then run broader checks proportional to regression risk.
6. Refactor only while the tests remain green.

Tests should be deterministic, readable, and resistant to implementation-only changes. Prefer real collaborators when cheap and reliable; use fakes or mocks at slow, unstable, destructive, or external boundaries. Avoid production APIs that exist only to support tests.

## When strict test-first is impractical

A test-first cycle may add little value for documentation, generated artifacts, configuration-only edits, exploratory spikes, or environments without a usable automated harness. Proceed without asking when the exception is clear, and record the alternative validation used. For legacy code that is hard to isolate, add the narrowest characterization or integration check that can expose the regression.

Do not delete correct pre-existing work merely because its tests were written later. Improve its evidence from the current state.

Apply `verification-before-completion` before claiming the behavior works or the regression is covered.
