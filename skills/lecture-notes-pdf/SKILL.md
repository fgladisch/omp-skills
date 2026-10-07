---
name: lecture-notes-pdf
description: Merge professor lecture notes with Deeptutor preview records into a pre-class 수업용 강의노트+요약 PDF. Use when the week's preview is done, before class.
---

# Lecture Notes PDF (수업 전: 예습 병합 → 수업용 강의노트)

Position in pipeline: 교수 강의노트 → Deeptutor 예습 → **본 스킬(병합 + 수업용 PDF)** → 수업 필기/녹음 → skills 3·4 (복습). This PDF is what the user brings to class.

## Inputs & merge (assistant does this; not automatic)

- ① 강의노트 원본.md — professor material (PDF면 skill 1 `lecture-md-convert`로 먼저 변환)
- ② Deeptutor 예습 기록.md — study chat log for the week
- Assistant merges ①+② into the builder content: keep the source structure and page refs (`p.N`); fold preview findings in as `예습 헷갈림` warn boxes and `한 줄 정리` cards. Never invent page refs; mark preview-derived boxes so class-time annotation can correct them.
- Pen memos go in as TEXT (`✎ 펜 메모 (p.N)` tip boxes), never ink-crop images; corrected texts live in the builder strings.

## Core module

`noteitmarkdown.print_layout.LecturePrintLayout(figure_dir, slice_dir)` (repo: `/tmp/noteitmarkdown/src/noteitmarkdown/print_layout.py`):

- `figrow(*names, caps=[...], tall=False)` — indivisible 2-column grid (one group stays together)
- `figstack(*rows)` — slice tall text-dense figures (2.5% overlap, deterministic hashed names) and recompose as indivisible rows
- `figure_group(title, content, fill=False)` — keep a heading with all its panels on one page; `fill=True` uses the `figure-fill` profile for dense groups
- `fig(name, cap)` — single figure; `document(body)` — wrap body HTML

## Builder pattern (per subject-week script)

- Constants `VAULT / SRC(=.../1주차 강의노트) / OUT(=.../1주차 본수업)`, `LAYOUT = LecturePrintLayout(SRC/"figures", Path("/tmp/<subject>-figure-slices"))`, then `build_notes() -> str` returning body HTML with `.headband/.cover/.goals/h2.sec/.card/.formula/.tip/.warn/table.kv` blocks.
- Sections mirror the lecture flow; each figure group gets its source pages in the title (e.g. `브라우저 연표 전반 (p.21)`).
- Split a group that overflows one page into 전반/후반 groups (verified case: 8 browser icons).
- Print via headless Chrome:
  ```
  /Applications/Google Chrome.app/Contents/MacOS/Google Chrome --headless=new --no-pdf-header-footer --disable-gpu --font-render-hinting=none --print-to-pdf=<OUT.pdf> file://<tmp.html>
  ```

## Gotchas

- exFAT volumes: lookup is normalization-insensitive but `unlink` needs the exact on-disk (NFD) name. Resolve via `os.listdir` + `unicodedata.normalize("NFC", …)` before deleting (see example builder `to_pdf`).
- Pen memos go in as TEXT (`✎ 펜 메모 (p.N)` tip boxes), never ink-crop images; corrected texts live in the builder strings.

## Example

`examples/internet_build.py` — full working builder (notes + worksheet + answers) for 인터넷과 메타버스 1주차.

## Verification

- pypdf text check: each `figure_group` title and all its captions on the same single page
- Render sample pages at 2x, assert content bounds clear of edges (20px+)
- Companion PDFs (worksheet/answers) all pages non-empty
