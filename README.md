# omp-skills

A personal skills library for [Oh My Pi](https://github.com/can1357/oh-my-pi). The skills target OMP's built-in tool surface and execution workflows.

## Installation

OMP discovers user skills one directory below `~/.omp/agent/skills/`. Clone the repository, then symlink each skill directory:

```sh
git clone https://github.com/fgladisch/omp-skills.git ~/.omp/omp-skills
mkdir -p ~/.omp/agent/skills
for skill in "$HOME"/.omp/omp-skills/skills/*; do
  ln -sfn "$skill" "$HOME/.omp/agent/skills/$(basename "$skill")"
done
```

For local development, replace `"$HOME"/.omp/omp-skills/skills/*` with the path to this checkout's `skills/*`. Restart OMP after adding or removing skills so discovery runs again.

## Skills

| Skill                            | When to use                                                                                                           |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `code-review`                    | When reviewing code                                                                                                   |
| `commit`                         | When the user asks to commit changes; follows repository conventions with gitmoji as the fallback                     |
| `finalizing-changes`             | When a coherent set of changes is ready to validate and then commit, merge, publish as a PR, or retain                |
| `planning`                       | When the user asks for a design or plan, or a change has consequential unresolved decisions                           |
| `systematic-debugging`           | When a bug, failing test, build failure, performance regression, or unexpected behavior needs diagnosis               |
| `test-driven-development`        | For behavior changes and bug fixes when a test or executable regression check can establish the expected result first |
| `verification-before-completion` | Before claiming work is complete, fixed, passing, reviewed, ready, committed, or integrated                           |

## Skill dependency graph

```mermaid
flowchart TB
  P["planning<br/>(when requested or decisions remain)"]
  SD["systematic-debugging"]
  TDD["test-driven-development"]
  CR["code-review"]
  V["verification-before-completion"]
  C["commit"]
  F["finalizing-changes"]

  P -. "clear implementation request" .-> TDD
  SD -. "when a regression cycle is feasible" .-> TDD
  TDD -. "when independent review adds value" .-> CR
  CR --> V
  TDD --> V
  SD --> V
  V --> C
  V --> F
```

Dashed edges are optional. Clear implementation requests can proceed without a planning ceremony, and review depth should match the size and risk of the change.

## OMP tooling

- `ask` provides structured decisions; no extension-provided selection tool is required.
- `read`, `glob`, `grep`, `lsp`, `edit`, and `write` handle repository inspection and changes before shell fallbacks.
- `debug` and `browser` verify runtime and UI behavior directly.
- `task`, `hub`, and `todo` provide parallel agents, process supervision, and phase tracking.
- Skills and their supporting files are addressable through `skill://<name>`.
- Project instructions live in `AGENTS.md`; OMP loads them as repository context.

## License

MIT — see [LICENSE](LICENSE).
