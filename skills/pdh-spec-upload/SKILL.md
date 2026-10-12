---
name: pdh-spec-upload
description: Use when the user wants to upload or replace one or more spec files (HTML, Markdown, PDF) on the PDH S3 API service on live, with or without a Jira ticket.
---

# Upload spec files to PDH S3 (live)

Uploads or replaces files on `https://pdh-s3-api-service.tooling.live.sipgate.net` and returns their public URLs.

## Rules

- Never print the API key. Never put it on a command line: send the header through stdin with `printf` (a shell builtin) and `curl -H @-`.
- Run every check before the first upload.
- Stop at the first failed request.

## Steps

### 1. Collect inputs

Get the local file paths and the ticket from the user.

- Ticket format: `^[A-Z][A-Z0-9]*-\d+$`, 1–63 chars, for example `PDH-1572`. If it is invalid, ask for a valid ticket or none.
- No ticket: ask once, "Store the files at `specs/<filename>` without a ticket?" Continue only on yes.

### 2. Check each file locally

- The file exists and is at most 10 MB (`wc -c < <path>`). If not, stop and report.
- Target name = local filename. It must be lowercase `[a-z0-9._-]`, 1–63 chars, with an extension, and must not end with a dot. If it is invalid, suggest a valid target name (for example `Spec Draft.HTML` → `spec-draft.html`) and use it only after the user approves. Do not rename the local file.
- Target names must be unique in one run. For a duplicate, suggest a different name and use it only after the user approves.
- If the extension is not `.html`, `.htm`, `.md`, or `.pdf`, warn: "This file type is served as a download, not shown in the browser." Continue.

### 3. Check the key

```bash
[ -n "${PDH_S3_SERVICE_API_KEY_LIVE:-}" ] && echo set || echo unset
```

If `unset`, ask the user to choose:

- **a)** The user exports the key before the agent starts and then confirms:
  `export PDH_S3_SERVICE_API_KEY_LIVE="$(op read 'op://rocwtt3yn4q4i6744vdfa7xb7q/PDH_S3_SERVICE_API_KEY_LIVE/credential')"`
- **b)** The agent reads the key inline with `op read` in the upload command (step 6). 1Password can ask the user to unlock.

### 4. Check which files exist

For each file, without a key (omit `<TICKET>/` when there is no ticket):

```bash
curl -s -o /dev/null -w '%{http_code}\n' "https://pdh-s3-api-service.tooling.live.sipgate.net/v1/specs/<TICKET>/<target-name>"
```

- `404`: new file.
- `200`: the file exists.
- Any other code: stop before any upload and report the code (see the error table).

### 5. Ask before an overwrite

If at least one file exists and the user did not ask to replace, list the existing files and ask once: "Overwrite all or abort?" On abort, stop without uploading.

### 6. Upload in one shell command

Set `K` from the environment variable (choice a or key already set):

```bash
K="$PDH_S3_SERVICE_API_KEY_LIVE"
```

or read it inline (choice b):

```bash
K="$(op read 'op://rocwtt3yn4q4i6744vdfa7xb7q/PDH_S3_SERVICE_API_KEY_LIVE/credential')"
```

Then run the uploads in the same command, chained with `&&`, so the chain stops at the first failure. Use `send` with `POST` for new files and `PUT` for existing files. Example with a ticket, one new and one existing file (for choice b, replace the first line with the `op read` line, followed by `&&`):

```bash
K="$PDH_S3_SERVICE_API_KEY_LIVE" &&
B=https://pdh-s3-api-service.tooling.live.sipgate.net/v1/specs &&
send() { n=$1; shift; c=$(printf 'X-Api-Key: %s\n' "$K" | curl -sS -o /dev/null -w '%{http_code}' -H @- "$@") || { echo "$n curl-failed"; return 1; }; echo "$n $c"; case $c in 2??) ;; *) return 1 ;; esac; } &&
send PDH-1572/spec.html -F "file=@./spec.html;filename=spec.html" "$B?ticket=PDH-1572" &&
send PDH-1572/notes.md -X PUT --data-binary @./notes.md "$B/PDH-1572/notes.md"
```

Without a ticket: `POST` to `"$B"` (no `?ticket=`), `PUT` to `"$B/<target-name>"`.

If `op read` fails, stop and tell the user to sign in to 1Password (`op signin`) with an account that can read the vault "AI Agents (Praxis Doktor Hasenbein)".

### 7. Report

For each uploaded file (omit `<TICKET>/` when there is no ticket), print `https://pdh-s3-api-service.tooling.live.sipgate.net/v1/specs/<TICKET>/<target-name>`. Do not use the `url` field from responses. List the files that were not uploaded and why.

## Errors

| Code          | Meaning                                  | Action                                                                         |
| ------------- | ---------------------------------------- | ------------------------------------------------------------------------------ |
| `000`         | No connection (existence check)          | Stop; report                                                                   |
| `curl-failed` | No connection or transfer error (upload) | Stop; report                                                                   |
| `400`         | Invalid ticket, filename, or body        | Stop; report                                                                   |
| `401`         | Key wrong or expired                     | Stop; tell the user to re-export `PDH_S3_SERVICE_API_KEY_LIVE`; offer choice b |
| `413`         | File larger than 10 MB                   | Stop; report                                                                   |
| `502`         | S3 storage unavailable                   | Stop; report; retry later                                                      |
| `507`         | S3 storage quota full                    | Stop; report                                                                   |
