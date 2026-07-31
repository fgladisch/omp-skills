---
name: systematic-debugging
description: Use when a bug, failing test, build failure, performance regression, or other unexpected behavior needs diagnosis before a fix is proposed.
---

# Systematic Debugging

Find evidence for the failure mechanism before changing production behavior. Use Oh My Pi's runtime tools to observe the real state instead of guessing.

## Reproduce

1. Read the complete error, logs, stack trace, and relevant configuration with `read`.
2. Reproduce the symptom with the smallest reliable command or interaction. Use `bash` for finite commands and `hub` for services, watchers, REPLs, or processes that need later interaction.
3. For UI failures, drive the exact path with `browser` and record the observed state.
4. If the failure is intermittent, record conditions and frequency rather than treating one pass as proof.

## Diagnose

1. Inspect recent changes, environment differences, and nearby working examples.
2. Use `lsp` to navigate definitions, implementations, types, and references. Use `grep` only when the relationship is textual rather than symbolic.
3. Use `debug` for breakpoints, stack frames, variables, threads, and stepping. Prefer it over adding speculative logging when a supported adapter can observe the state directly.
4. Trace incorrect data or state backward across component boundaries. Capture inputs and outputs without exposing secrets.
5. State one falsifiable hypothesis: suspected cause, supporting evidence, and a result that would disprove it.
6. Run the smallest experiment that distinguishes that hypothesis from alternatives.

Do not mix speculative fixes into evidence gathering. A disproved hypothesis is progress; update it from the new evidence.

## Fix

Once the cause is supported:

1. Add a focused regression test or executable reproduction when feasible.
2. Change the source of the fault with the smallest sufficient `edit`; use `lsp` for symbol-aware changes and code actions.
3. Re-run the original reproduction and confirm the symptom no longer occurs.
4. Run the focused regression check and broader checks proportional to the affected area.
5. Remove temporary diagnostics and stop temporary `hub` processes unless they provide lasting operational value.

Use `test-driven-development` when a reliable red-green cycle is feasible. Apply `verification-before-completion` before reporting the bug fixed.

## Escalate

Report an evidence gap only when reproduction requires unavailable access, data, hardware, or credentials. Ask before broad architectural work or scope expansion. Report the root cause, evidence, change, verification, and remaining uncertainty.
