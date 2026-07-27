# Prettier Configuration Design

## Goal

Make Markdown formatting deterministic while preserving existing prose wrapping and Prettier-aligned Markdown tables.

## Scope

- Add a tracked `.prettierrc.json` with `proseWrap` set to `preserve`.
- Update the repository's local `.git/hooks/pre-commit` hook to run Prettier 3.9.6.
- Reformat every tracked Markdown file with Prettier 3.9.6 using the tracked configuration.
- Include this design document, the formatting changes, and the configuration in the existing Markdown formatting commit.

The formatting corpus is the Markdown paths returned by `git ls-files '*.md'`, plus this design document before it is first staged. Ignored generated artifacts and unrelated untracked Markdown are excluded. The local hook remains outside version control. No package manifest, lockfile, hook installer, or shared hook framework will be added.

## Configuration

The repository root will contain:

```json
{
  "proseWrap": "preserve"
}
```

`preserve` retains the prose line structure already present in each file. Because the existing formatting pass removed unnecessary prose line breaks, those paragraphs remain unwrapped. Prettier will continue to align Markdown table columns.

## Pre-commit Hook

The existing local hook will replace `prettier@3.6.2` with `prettier@3.9.6`. Pinning the version keeps local commits deterministic and avoids unexpected formatting changes when a new Prettier release is published.

The hook will keep its current behavior:

- Process staged Markdown files only.
- Refuse partially staged Markdown files before autoformatting.
- Format eligible files and stage the formatter output.

## Verification

Implementation is accepted when:

1. Prettier 3.9.6 reports every Markdown file in the defined formatting corpus as formatted using the repository configuration.
2. Re-running Prettier 3.9.6 produces no changes.
3. The local pre-commit hook references `prettier@3.9.6`.
4. Markdown tables remain aligned.
5. `git diff --check` reports no whitespace errors.
