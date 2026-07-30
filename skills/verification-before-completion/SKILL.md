---
name: verification-before-completion
description: Use before claiming work is complete, fixed, passing, reviewed, ready, committed, or integrated; match each material claim to fresh evidence.
---

# Verification Before Completion

Report the state proven by current evidence. Do not turn expectations or delegated reports into success claims.

## Verification gate

Before a material completion or correctness claim:

1. Identify the evidence that would prove it.
2. Run the relevant command or inspect the authoritative artifact after the final change.
3. Check the exit status and read enough output to detect failures, skipped coverage, or partial execution.
4. Compare the result with the request and repository conventions.
5. State the result with the evidence. If validation failed or could not run, report that limitation directly.

Choose checks proportional to the change and risk. A focused documentation edit may need formatting, link, and diff checks. Runtime behavior may need focused tests plus a broader suite, build, typecheck, or lint command. Do not run unrelated expensive suites solely to satisfy a ritual.

## Delegated work

Treat subagent reports as leads. Inspect the resulting diff or artifact and independently run the checks needed for the final claim.

## Reporting

Lead with the result. Include the commands or artifacts that support it, material caveats, and the next action when work remains. Avoid “should pass,” “looks correct,” or equivalent wording when the evidence is absent.
