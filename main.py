#!/usr/bin/env python3
"""Unsent: The Micro-Confession Sprint — two-part micro-confession.

Writes a "To:" line plus the unsent message itself to entry.txt,
with no trailing newline and no explanation after it.
"""

import os
import tempfile

ENTRY_TEXT = (
    "To: Mom\n"
    "I told you I quit the job because I wanted a break. "
    "The truth is they let me go in March and I've been "
    "pretending ever since."
)


def main() -> None:
    # Enforce the competition gate before writing anything.
    lines = ENTRY_TEXT.split("\n")
    if len(lines) != 2 or not lines[0].startswith("To: "):
        raise ValueError("entry must be a To: line plus one message line")
    if len(ENTRY_TEXT) > 260:
        raise ValueError("entry exceeds 260 characters")
    if len(lines[1]) > 200:
        raise ValueError("message line exceeds 200 characters")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    target = os.path.join(output_dir, "entry.txt")
    data = ENTRY_TEXT.encode("utf-8")
    fd, tmp_path = tempfile.mkstemp(dir=output_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, target)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except FileNotFoundError:
            pass
        raise


if __name__ == "__main__":
    main()
