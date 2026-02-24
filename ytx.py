#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "youtube-transcript-api",
#   "pyperclip",
#   "tabulate",
# ]
# ///

import argparse
import sys
from datetime import datetime

import pyperclip
from tabulate import tabulate
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    CouldNotRetrieveTranscript,
    TranscriptsDisabled,
    VideoUnavailable,
)

PRECEDENCE = [
    (False, "pl"),  # manual + pl
    (False, "en"),  # manual + en
    (True, "pl"),   # generated + pl
    (True, "en"),   # generated + en
]


def error(msg):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def fetch_transcript_list(video_id):
    try:
        ytt_api = YouTubeTranscriptApi()
        return ytt_api.list(video_id)
    except VideoUnavailable:
        error(f"Video not found: {video_id}")
    except TranscriptsDisabled:
        error(f"Transcripts are disabled for video: {video_id}")
    except CouldNotRetrieveTranscript:
        error(f"Could not retrieve transcripts for video: {video_id}")
    except Exception as e:
        error(f"Failed to fetch transcripts: {e}")


def get_transcript_entries(transcript_list):
    entries = []
    for t in transcript_list:
        entries.append({
            "language_code": t.language_code,
            "language": t.language,
            "is_generated": t.is_generated,
            "transcript": t,
        })
    return entries


def select_by_precedence(entries):
    for is_generated, lang in PRECEDENCE:
        for entry in entries:
            if entry["is_generated"] == is_generated and entry["language_code"].startswith(lang):
                return entry
    return None


def fetch_transcript(transcript_obj):
    snippets = transcript_obj.fetch()
    return " ".join(snippet.text for snippet in snippets)


def format_info_table(entries):
    rows = []
    for i, entry in enumerate(entries):
        rows.append([
            i,
            entry["language_code"],
            entry["language"],
            "generated" if entry["is_generated"] else "manual",
        ])
    return tabulate(rows, headers=["idx", "lang_code", "language", "type"], tablefmt="simple")


def build_filename(video_id, is_generated, lang_code):
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    type_str = "gen" if is_generated else "man"
    return f"/tmp/ytx-{ts}-{type_str}{lang_code}-{video_id}.txt"


def save_and_copy(text, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    pyperclip.copy(text)


def main():
    parser = argparse.ArgumentParser(
        prog="ytx",
        description="Download YouTube video transcripts as plain text.",
    )
    parser.add_argument("video_id", help="YouTube video ID (e.g. dQw4w9WgXcQ)")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--info", action="store_true", help="List available transcripts")
    group.add_argument("-f", "--fetch", type=int, metavar="N", help="Fetch transcript at index N from -i table")

    args = parser.parse_args()

    transcript_list = fetch_transcript_list(args.video_id)
    entries = get_transcript_entries(transcript_list)

    if not entries:
        error("No transcripts available for this video.")

    if args.info:
        print(format_info_table(entries))
        sys.exit(0)

    if args.fetch is not None:
        if args.fetch < 0 or args.fetch >= len(entries):
            error(f"Index {args.fetch} out of range. Available: 0-{len(entries) - 1}")
        selected = entries[args.fetch]
    else:
        selected = select_by_precedence(entries)
        if selected is None:
            print("No matching transcript found (pl/en, manual/generated).", file=sys.stderr)
            print("Available transcripts:", file=sys.stderr)
            print(format_info_table(entries), file=sys.stderr)
            sys.exit(1)

    text = fetch_transcript(selected["transcript"])
    filepath = build_filename(args.video_id, selected["is_generated"], selected["language_code"])
    save_and_copy(text, filepath)
    print(f"Saved: {filepath}")


if __name__ == "__main__":
    main()
