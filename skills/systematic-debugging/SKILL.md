---
name: systematic-debugging
description: Use when a bug, failing test, build failure, performance regression, or other unexpected behavior needs diagnosis before a fix is proposed.
---

# Systematic Debugging

Find evidence for the failure mechanism before changing production behavior.

## Diagnose

1. Read the complete error, logs, and stack trace.
2. Reproduce the symptom with the smallest reliable command or sequence. If it is intermittent, record the observed conditions instead of guessing.
3. Inspect recent changes, environment differences, configuration, and nearby working examples.
4. Trace incorrect data or state backward to its source. At component boundaries, capture inputs and outputs while avoiding secrets.
5. State one falsifiable hypothesis: the suspected cause, the evidence supporting it, and the result that would disprove it.
6. Run the smallest experiment that distinguishes this hypothesis from alternatives.

Do not mix speculative fixes into evidence gathering. When an experiment disproves the hypothesis, update it from the new evidence.

## Fix

Once the cause is supported:

1. Add a focused regression test or executable reproduction when feasible.
2. Change the source of the fault with the smallest sufficient patch.
3. Verify the original symptom, the focused regression check, and broader checks proportional to the affected area.
4. Remove temporary diagnostics unless they provide lasting operational value.

Use `test-driven-development` when an automated failing check or executable regression cycle is feasible. Apply `verification-before-completion` before reporting the bug fixed.

## Escalate

Stop and report the evidence gap when reproduction requires unavailable access, data, hardware, or credentials. Reconsider the design when repeated well-supported hypotheses fail or each attempted fix exposes a different coupling problem. Ask before broad architectural work or scope expansion.

Report the root cause, evidence, change, verification, and any remaining uncertainty.
