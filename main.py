#!/usr/bin/env python3
"""Unsent: The Micro-Confession Sprint entry.

Writes one two-part micro-confession to ``entry.txt`` in the output
directory (``$MAKEFUN_OUTPUT_DIR``, default ``/output``): a ``To:`` line
naming who it was meant for, and the unsent line itself, exactly as typed.

The confession: a son who learned his mother's soup the week she went
into hospital and has cooked it every Sunday since, still unable to tell
her he was practising for the day she won't be here to make it.
Deterministic, offline, no input read.
"""

import os

ENTRY = (
    "To: Mom\n"
    "I learned to make your soup the week you went into hospital, and "
    "I've made it every Sunday since, but I still can't tell you I was "
    "practicing for the day you won't be here to make it."
)

MAX_CHARS = 260
MAX_MESSAGE_CHARS = 200


def validate(text: str) -> None:
    """The gate only accepts UTF-8 text of 1 to 260 characters, not only
    whitespace. The judge's brief caps the message itself at 200
    characters, and the entry must be exactly two parts: a To: line and
    one message line, with no explanation after it. Fail loudly here
    instead of shipping an entry the judge never sees."""
    assert isinstance(text, str)
    assert 1 <= len(text) <= MAX_CHARS, f"entry is {len(text)} chars, must be 1-{MAX_CHARS}"
    assert text.strip(), "entry must not be only whitespace"
    lines = text.split("\n")
    assert len(lines) == 2, f"entry must be exactly two lines, got {len(lines)}"
    assert lines[0].startswith("To: "), "first line must be a To: line"
    assert lines[0][4:].strip(), "To: line must name someone"
    assert 1 <= len(lines[1]) <= MAX_MESSAGE_CHARS, (
        f"message is {len(lines[1])} chars, must be 1-{MAX_MESSAGE_CHARS}"
    )
    assert "\r" not in text, "entry must not contain carriage returns"


def main() -> None:
    validate(ENTRY)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(ENTRY)
    print(f"wrote {len(ENTRY)} characters to {path}")


if __name__ == "__main__":
    main()
