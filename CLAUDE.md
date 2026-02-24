# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ytx** is a Python CLI tool that downloads YouTube video transcripts as plain text, saves them to `/tmp`, and copies to clipboard. Designed for desktop use as input to TTS/LLM pipelines. Uses `youtube-transcript-api` (not YT Data API v3).

## Dependencies & Package Management

Single-file script using **PEP 723 inline script metadata** (no `pyproject.toml`). Dependencies are declared in the script header and resolved automatically by `uv run --script`.

Key dependencies:
- `youtube-transcript-api` — transcript fetching (instance-based API: `YouTubeTranscriptApi()`)
- `pyperclip` — clipboard
- `tabulate` — table output

## CLI Interface

```sh
./ytx.py <video_id>           # Fetch by precedence, save file, copy to clipboard
./ytx.py <video_id> -i        # List available transcripts as table
./ytx.py <video_id> -f <N>    # Fetch transcript at index N from -i table
./ytx.py -h                   # Help
```

`<video_id>` is a bare ID (e.g. `dQw4w9WgXcQ`), not a full URL. Flags `-i` and `-f` are mutually exclusive.

## Transcript Selection Precedence (without `-f`)

1. manual + pl
2. manual + en
3. generated + pl
4. generated + en

Other languages are ignored in automatic selection.

## Output File Naming

```
/tmp/ytx-{YYYYMMDDhhmmss}-{type}{lang}-{video_id}.txt
```

`{type}` = `man` | `gen`, `{lang}` = language code. Example: `/tmp/ytx-20260224164354-manpl-GAi05PYGTS4.txt`

## Error Handling

All errors go to stderr with non-zero exit. On error: no file created, no clipboard modified.

## Code Conventions

- All code comments and descriptions in English
- PRD is in Polish (PRD.md)
