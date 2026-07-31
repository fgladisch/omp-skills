---
name: verification-before-completion
description: Use before claiming work is complete, fixed, passing, reviewed, ready, committed, or integrated; match each material claim to fresh evidence.
---

# Verification Before Completion

Report only the state proven by fresh evidence. Expectations, stale output, and subagent reports are not completion evidence.

## Build the evidence map

Before a material claim:

1. Name the observable evidence that would prove it.
2. Run or inspect that evidence after the final change.
3. Check exit status and enough output to catch failures, skipped coverage, partial execution, or the wrong target.
4. Compare the result with every acceptance criterion and repository convention.
5. State exactly what passed, failed, or could not run.

Use the OMP tool that exercises the real boundary:

- `bash` for focused tests, builds, type checks, linters, and finite CLI smoke tests;
- `lsp` diagnostics for current language-server errors, never as a substitute for runtime validation;
- `hub` to start and observe long-running services;
- `browser` to exercise changed UI behavior and inspect the rendered result;
- `read` to inspect generated artifacts, documents, URLs, `pr://`, or `issue://`;
- `debug` when the claim depends on runtime state that ordinary output cannot establish.

Choose checks proportional to the change and risk. Run the changed path through its real entry point. Do not run an unrelated expensive suite solely as a ritual.

## Delegated work

Treat `task` results as leads. Inspect the resulting artifact and independently run the checks required for the final claim. A completed agent job proves only that the agent returned.

## Completion gate

Confirm all `todo` acceptance items are complete. If any item is blocked, report that work remains and do not claim completion. Stop temporary `hub` processes, and confirm affected callsites, tests, documentation, and generated artifacts are updated or intentionally unchanged.

## Reporting

Lead with the result. Cite the commands or authoritative artifacts that support each material claim, include material caveats, and give the next concrete action when work remains. Never write “should pass,” “looks correct,” or equivalent language without evidence.
