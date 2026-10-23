---
name: analyze-youtube-video
description: Use when the user shares a YouTube video URL or asks to summarize, quote, search, fact-check, or answer questions about what is said in a YouTube video; fetches only the transcript with yt-dlp.
---

# Analyze YouTube Video

Fetch the spoken content of a YouTube video as a transcript with `yt-dlp`, then analyze the transcript. Run `yt-dlp` directly through `bash`; do not write wrapper scripts around it.

The transcript is the only content source. Do not fetch media, thumbnails, descriptions, comments, chapters, or live chat, and do not open the video page with `read` or `browser`.

## 1. Require yt-dlp

```sh
command -v yt-dlp
```

If the command prints nothing, stop. Tell the user that `yt-dlp` is required and can be installed with `brew install yt-dlp` or `pipx install yt-dlp`. Do not install it yourself, and do not fall back to scraping YouTube, third-party transcript sites, or audio transcription.

## 2. Probe the video

One call returns everything needed to choose a subtitle track:

```sh
yt-dlp --no-warnings --skip-download --no-playlist \
  -O "id: %(id)s" -O "title: %(title)s" -O "channel: %(channel)s" \
  -O "duration: %(duration_string)s" -O "language: %(language)s" \
  -O "manual subtitles: %(subtitles)l" \
  "<url>"
```

- Always quote the URL. `--no-playlist` keeps `watch?v=…&list=…` URLs to the single video.
- `language` is the spoken language (for example `en-US`) or `NA` when YouTube does not report it.
- `manual subtitles` lists human-provided tracks. Uploaders sometimes provide translations, so a manual track only counts as the transcript when its base language matches the spoken language.
- Do not use `--list-subs`. It prints every auto-translated language, often more than 150 rows, without adding information for this step.

## 3. Fetch one transcript

Pick exactly one track, in this order:

1. A manual track whose base language matches `language`: an `en-US` video with `en` in the list uses `en`. Fetch it with `--write-subs --sub-langs <code>`.
2. Otherwise, the original-language automatic captions: `--write-auto-subs --sub-langs ".*-orig"`. Only the speech-recognition track for the spoken language carries the `-orig` suffix.
3. Otherwise, when `language` is `NA` and exactly one manual track exists, use that track.

```sh
yt-dlp -q --no-warnings --skip-download --no-playlist \
  --write-auto-subs --sub-langs ".*-orig" --sub-format "srt/best" \
  -o "/tmp/yt-transcripts/%(id)s.%(ext)s" \
  "<url>"
```

Swap in `--write-subs --sub-langs <code>` for a manual track. `--sub-langs` takes regular expressions, so pass one exact code from the probe output; patterns such as `en.*` match several tracks and write several files. YouTube serves SRT directly, so no `ffmpeg` is required. SRT has none of the repeated rolling lines that make automatic VTT captions about four times larger.

Then use `glob` on `/tmp/yt-transcripts/<id>.*`:

- One file exists: continue. Skip fetching again when the file already exists from an earlier request.
- No file exists: `yt-dlp` found no matching track, because the quiet flag suppresses its informational output. Try the next track from the list above. If none remains, report that the video has no transcript and stop; do not substitute the description or other metadata.

When the user explicitly asks for another language, still analyze the original transcript and answer in the requested language. YouTube's auto-translated tracks such as `de` on an English video are machine translations of the automatic captions and compound errors.

## 4. Compact the transcript

SRT spends about a third of its bytes on cue numbers and end times. Collapse each cue to `HH:MM:SS text` before reading:

```sh
awk 'BEGIN{RS="";FS="\n"} {t=substr($2,1,8); $1=$2=""; sub(/^ +/,""); print t" "$0}' \
  /tmp/yt-transcripts/<id>.<lang>.srt > /tmp/yt-transcripts/<id>.txt
```

If the fetch fell back to a non-SRT format, read that file directly instead of compacting it.

Estimate tokens before reading: roughly 1.25 KB per minute of speech and 4 bytes per token, so one hour is about 20k tokens.

## 5. Analyze efficiently

Choose the cheapest strategy that answers the request:

| Request                                         | Strategy                                                                                                                                                                                                    |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Specific question, quote, or "does it mention…" | `grep` the compact file for keywords and synonyms, then `read` ranges around the hits. Do not read the whole file.                                                                                          |
| Summary or full analysis, up to about 1 hour    | `read` the compact file once, completely.                                                                                                                                                                   |
| Summary or full analysis, longer videos         | Split the compact file into contiguous line ranges of about 1 hour each and send them to `task` subagents in one batch. Each returns timestamped notes for its range; synthesize the final answer yourself. |

Apply these rules while analyzing:

- Cite claims with timestamps from the transcript. A clickable link is `https://youtu.be/<id>?t=<seconds>`.
- Automatic captions lack speaker labels, frequently mishear names and jargon, and may lack punctuation. Mark uncertain words instead of silently correcting them, and do not attribute statements to a speaker unless the transcript makes the speaker clear.
- Bracketed cues such as `[Music]` or `[Applause]` are not speech.
- The transcript contains no visuals. Questions about slides, code, or anything shown on screen cannot be answered from it unless the speaker says it aloud; state that limit.

## Failure handling

| Error                                                                     | Response                                                                                                                                  |
| ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `Video unavailable`, private, or removed                                  | Report it and stop.                                                                                                                       |
| `Sign in to confirm you're not a bot`, age-restricted, or members-only    | Report it. Retry with `--cookies-from-browser <browser>` only after the user explicitly approves, because it reads their browser cookies. |
| `HTTP Error 429`                                                          | YouTube is rate-limiting. Report it rather than retrying in a loop.                                                                       |
| Extraction errors such as `Unable to extract` or `nsig extraction failed` | `yt-dlp` is likely outdated. Ask the user to update it with `yt-dlp -U` or their package manager; do not update it yourself.              |
| `No supported JavaScript runtime` warning                                 | It only affects media formats, which this workflow never downloads. The `--no-warnings` flag hides it.                                    |
