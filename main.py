#!/usr/bin/env python3
"""Third Coil, A3 -- make.fun entry for "One Line, One Minute: The
Vending Machine Pickup Line Contest".

Writes one pickup line, spoken by a vending machine to a passing
human, to ``entry.txt`` inside the output directory
(``$MAKEFUN_OUTPUT_DIR``, default ``/output``).

The line is fixed text, kept as one constant so the program is fully
deterministic: the grader runs it twice and the two runs must agree
byte for byte. Before anything is written, validate_entry() enforces
the sealed scorer's gate exactly as RULES.txt states it: the file must
be UTF-8 text of 1 to 200 characters, and not only white space. After
writing, the file is read back and checked again -- what lands on disk
is what the judge sees, so the written bytes are verified, not just
the constant in memory.

Why this line works as a pickup from a machine: it opens with a
promise the machine can literally keep ("I'd drop everything for
you"), then turns it -- the drop is a stuck snack in the third coil,
slot A3. The machine flirts the only way it knows how: with its own
world of coils, slots and exact change, and the joke lands because
the grand romantic gesture is also a vending-machine malfunction.
The last four words do the work: "and it's stuck" turns the promise
into a confession, and the machine is charming precisely because it
cannot deliver what it just offered -- it can only drop things, and
even that is jammed.
"""

import os

ENTRY = (
    "I'd drop everything for you. "
    "Literally. Third coil, A3... and it's stuck."
)

MAX_CHARS = 200


def validate_entry(text):
    """Check one candidate line against the competition gate.

    Returns (ok, reason): reason is empty when the text is valid.
    """
    if not isinstance(text, str):
        return False, "entry is not text"
    if not text.strip():
        return False, "entry is empty or only white space"
    if len(text) > MAX_CHARS:
        return False, "entry is %d chars, over the 200-char limit" % len(text)
    if text != text.strip():
        return False, "entry must not start or end with white space"
    if "\n" in text or "\r" in text:
        return False, "entry must be a single line"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False, "entry is not valid UTF-8 text"
    return True, ""


def resolve_output_dir():
    """The directory that receives entry.txt."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main():
    ok, reason = validate_entry(ENTRY)
    if not ok:
        raise SystemExit("invalid entry: %s" % reason)

    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the judged text is exactly this line, byte
    # for byte, with nothing extra for the judge to read.
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(ENTRY)

    with open(out_path, "r", encoding="utf-8") as handle:
        written = handle.read()
    ok, reason = validate_entry(written)
    if not ok or written != ENTRY:
        raise SystemExit(
            "round-trip check failed: file does not match the entry (%s)"
            % reason
        )

    print("wrote %s (%d chars)" % (out_path, len(ENTRY)))


if __name__ == "__main__":
    main()
