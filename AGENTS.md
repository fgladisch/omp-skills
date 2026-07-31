# AGENTS.md

Project context for agents working in this repository (`omp-skills`).

## Golden rule: keep skills and `README.md` in sync

The `## Skills` table in `README.md` is the human-facing index of every skill in this repo. It **must** stay in sync with the actual skill directories. Whenever you make any of the following changes, update `README.md` in the same change:

- **Adding a skill** — create `skills/<skill-name>/SKILL.md` _and_ add a row to the `## Skills` table in `README.md`. Insert the row in alphabetical order by skill name.
- **Removing a skill** — delete the directory _and_ remove its row from the table.
- **Renaming a skill** — rename the directory _and_ update the row (name + link target if any).
- **Changing what a skill is for** — if you materially change the `description` in a skill's frontmatter (the "When to use" summary), update the matching row in the table so they tell the same story.

The "When to use" column in `README.md` should be a short, human-readable rephrasing of the skill's frontmatter `description`. It does not have to be a verbatim copy, but it must not contradict it.

### How to verify sync

Before finishing any change that touches skills:

1. List skill directories: `ls -1 skills | grep -v '^\.'`
2. Compare against the rows in the `## Skills` table in `README.md`.
3. Every directory must have exactly one row, and every row must point to an existing directory.
4. For each row, skim the corresponding `SKILL.md` frontmatter `description` and confirm the "When to use" column still matches.

If any of those checks fail, fix `README.md` (or the skill) before considering the task done.

## Skill file conventions

- Each skill lives in its own directory: `skills/<skill-name>/SKILL.md`.
- `SKILL.md` starts with YAML frontmatter containing `name` and `description`. OMP exposes the description in discovered skill metadata and uses it to decide when to load the skill, so keep it precise and trigger-oriented.
- Supporting files (references, templates, examples) live alongside `SKILL.md` in the same directory and are referenced by relative path.

## Oh My Pi conventions used in this repo

- OMP auto-loads `AGENTS.md` as project context. Prefer `AGENTS.md` for repository instructions.
- Native skills are discovered from `~/.omp/agent/skills/` for users and `.omp/skills/` for projects. Each skill directory must be exactly one level below the discovery root.
- Tool names in skills follow OMP's built-in surface: `read`, `glob`, `grep`, `lsp`, `edit`, `write`, `bash`, `eval`, `ask`, `task`, `hub`, `todo`, `browser`, `debug`, and discoverable tools such as `ast_edit`.
