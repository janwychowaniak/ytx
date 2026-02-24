# ytx

CLI tool that downloads YouTube video transcripts as plain text, saves them to `/tmp`, and copies to clipboard. Designed as input to TTS/LLM pipelines.

## Requirements

- [uv](https://docs.astral.sh/uv/) — dependencies are resolved automatically on first run (PEP 723 inline script metadata)

## Usage

```sh
./ytx.py <video_id>           # Fetch by precedence, save file, copy to clipboard
./ytx.py <video_id> -i        # List available transcripts
./ytx.py <video_id> -f <N>    # Fetch transcript at index N from -i table
./ytx.py -h                   # Help
```

`<video_id>` is a bare YouTube ID (e.g. `dQw4w9WgXcQ`), not a full URL.

### Examples

List available transcripts:

```
$ ./ytx.py dQw4w9WgXcQ -i
  idx  lang_code    language                  type
-----  -----------  ------------------------  ---------
    0  en           English                   manual
    1  de-DE        German (Germany)          manual
    2  ja           Japanese                  manual
    3  pt-BR        Portuguese (Brazil)       manual
    4  es-419       Spanish (Latin America)   manual
    5  en           English (auto-generated)  generated
```

Fetch by automatic precedence:

```
$ ./ytx.py dQw4w9WgXcQ
Saved: /tmp/ytx-20260224143855-manen-dQw4w9WgXcQ.txt
```

Fetch a specific transcript by index:

```
$ ./ytx.py dQw4w9WgXcQ -f 2
Saved: /tmp/ytx-20260224144012-manja-dQw4w9WgXcQ.txt
```

## Transcript Selection Precedence

When no `-f` flag is given, transcripts are selected automatically:

1. manual + pl
2. manual + en
3. generated + pl
4. generated + en

Other languages are ignored. If no match is found, the tool prints available transcripts to stderr and exits with an error.

## Output

- File saved to `/tmp/ytx-{YYYYMMDDhhmmss}-{type}{lang}-{video_id}.txt`
- Plain text copied to clipboard
- `{type}` = `man` (manual) or `gen` (auto-generated)
