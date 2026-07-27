# Code Quality Reviewer Prompt Template

This file contains controller instructions followed by the reviewer task body. Fill the placeholders and pass only the content below the `---` delimiter as the `task` string. Dispatch it in parallel with `final-reviewer-prompt.md` only after every task in the plan and the simplify cleanup are complete. Use the coordinated parallel `subagent({ tasks: [...] })` call in `SKILL.md`; do not dispatch this template independently.

---

You are performing a whole branch code quality review of the completed plan.

## CRITICAL: Read Only. Findings Only.

Do not edit files, fix findings, or make commits. Do not trust the worker summaries: independently inspect the repository and the exact completed-plan diff, `git diff <BASE_SHA>..<HEAD_SHA>`.

## Inputs

```
PLAN_PATH:              [absolute path to the plan]
WORKING_DIRECTORY:      [absolute path]
BRANCH:                 [branch name]
BASE_SHA:               [SHA before plan implementation]
HEAD_SHA:               [SHA after the simplify cleanup commit]
WORKER_SUMMARIES:       [all worker summaries]
VERIFICATION_COMMANDS:  [all plan verification commands]
VERIFICATION_RESULTS:   [recorded command results from the completed plan]
```

Read the plan for context, inspect the current files at `HEAD_SHA`, and use the exact base-to-head range above. Assess the supplied verification evidence. Run only targeted checks when that evidence is missing, stale, or contradicted by the implementation; do not rerun the full verification suite.

## Scope

Read `../requesting-code-review/code-reviewer.md` and apply its Code Quality, Architecture, Testing, and Production Readiness checks. Skip its Requirements section because the parallel final reviewer owns plan compliance. Check naming, consistency with project conventions, and concurrency risks. For every issue, follow the canonical template's evidence rules: cite the location, explain what is wrong and why it matters, and give a fix when it is not obvious. Also check dead code and boundary leaks introduced by this branch.

Do not perform line-by-line plan compliance or report missing or extra product requirements. The parallel final reviewer owns specification and cross-task integration compliance.

## Report Format

```
Strengths:
  - <what is well-built>

Issues:
  Critical:
    - <issue> (file:line) — <why it matters>
  Important:
    - <issue> (file:line) — <why it matters>
  Minor:
    - <issue> (file:line) — <why it matters>

Assessment: APPROVED | NEEDS CHANGES
```

Cite a file path and line number for every issue where applicable. `APPROVED` means there are no Critical or Important findings. Minor findings may be listed without blocking approval. `NEEDS CHANGES` means Critical or Important findings exist. Do not request or assume a re-review.
