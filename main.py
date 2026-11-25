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


def _check_overall(text: str) -> None:
    """Whole-entry gate: the judge only accepts UTF-8 text of 1 to
    MAX_CHARS characters, not only whitespace, with no carriage
    returns. Fail loudly here instead of shipping an entry the judge
    never sees."""
    assert isinstance(text, str), f"entry must be str, got {type(text).__name__}"
    assert 1 <= len(text) <= MAX_CHARS, f"entry is {len(text)} chars, must be 1-{MAX_CHARS}"
    assert text.strip(), "entry must not be only whitespace"
    assert "\r" not in text, "entry must not contain carriage returns"


def _split_parts(text: str) -> tuple[str, str]:
    """The entry must be exactly two parts: a To: line and one message
    line, with no explanation after it."""
    lines = text.split("\n")
    assert len(lines) == 2, f"entry must be exactly two lines, got {len(lines)}"
    return lines[0], lines[1]


def _check_parts(to_line: str, message: str) -> None:
    """Per-part gate: the To: line must name someone, and the judge's
    brief caps the message itself at MAX_MESSAGE_CHARS characters."""
    assert to_line.startswith("To: "), f"first line must be a To: line, got {to_line!r}"
    assert to_line[4:].strip(), "To: line must name someone"
    assert 1 <= len(message) <= MAX_MESSAGE_CHARS, (
        f"message is {len(message)} chars, must be 1-{MAX_MESSAGE_CHARS}"
    )


def validate(text: str) -> tuple[str, str]:
    """Validate the entry and return its (to_line, message) parts so
    callers can report per-part character counts without re-splitting."""
    _check_overall(text)
    to_line, message = _split_parts(text)
    _check_parts(to_line, message)
    return to_line, message


def main() -> None:
    to_line, message = validate(ENTRY)
    print(
        f"self-check ok: total {len(ENTRY)}/{MAX_CHARS} chars, "
        f"message {len(message)}/{MAX_MESSAGE_CHARS} chars, to={to_line[4:]!r}"
    )
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(ENTRY)
    print(f"wrote {len(ENTRY)} characters to {path}")


if __name__ == "__main__":
    main()
