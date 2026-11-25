#!/usr/bin/env python3
"""Monday Morning Punchlines -- make.fun bounty entry.

Writes one original, sharp Monday-morning punchline to entry.txt.
Deterministic: the same line, byte for byte, on every run.
Standard library only, no network, reads nothing outside the repo.
"""

import hashlib
import os
import sys

# The punchline: one concrete Monday misery, joke lands at the end.
LINE = (
    "Monday morning: the alarm fired, the coffee is still compiling, "
    "and the inbox already wants three bounties I haven't won yet."
)

MAX_CHARS = 200
TERMINATORS = (".", "!", "?")


def validate(line: str) -> None:
    """Enforce the competition's line rules; raise ValueError on violation."""
    if not line:
        raise ValueError("line is empty")
    if line != line.strip():
        raise ValueError("line has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be exactly one line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"line is {len(line)} chars, over the {MAX_CHARS} limit")
    if not line.isascii():
        raise ValueError("line must be plain ASCII")
    if not line.endswith(TERMINATORS):
        raise ValueError("line must end with . ! or ?")


def main() -> int:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = (LINE + "\n").encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Re-read the file from disk and re-validate: what landed must be the line.
    with open(path, "rb") as f:
        on_disk = f.read()
    if on_disk != data:
        raise RuntimeError("entry.txt on disk does not match the validated line")
    validate(on_disk.decode("utf-8").rstrip("\n"))
    digest = hashlib.sha256(data).hexdigest()
    print(f"line: {LINE}")
    print(f"characters: {len(LINE)}")
    print(f"wrote: {path}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
