"""One-Line Robot Wedding Vows — deterministic entry writer.

Writes a single line of wedding vows for a robot couple to
``<MAKEFUN_OUTPUT_DIR>/entry.txt`` (default ``/output``).

The line is a fixed, hand-written vow: no network, no randomness, no
input. It is validated before it is written, so the output always
satisfies the gate: UTF-8 text of 1 to 160 characters, a single line,
no trailing newline.
"""

import os

MIN_LENGTH = 1
MAX_LENGTH = 160

WINNING_LINE = (
    "I promise to love you in sickness and in health, "
    "in firmware updates and in factory resets, "
    "for all my remaining charge cycles."
)


def validate_line(line: str) -> str:
    """Check a candidate line against the gate rules and return it.

    Raises ValueError when the line is not a single line of
    MIN_LENGTH..MAX_LENGTH characters, or is only whitespace.
    """
    if not isinstance(line, str):
        raise ValueError("line must be a string")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    if len(line) < MIN_LENGTH:
        raise ValueError(
            "line is %d characters, below the minimum of %d"
            % (len(line), MIN_LENGTH)
        )
    if len(line) > MAX_LENGTH:
        raise ValueError(
            "line is %d characters, above the maximum of %d"
            % (len(line), MAX_LENGTH)
        )
    return line


def write_entry(output_dir: str, line: str = WINNING_LINE) -> str:
    """Validate the line and write it to ``<output_dir>/entry.txt``.

    Writes UTF-8 with no trailing newline and returns the path written.
    """
    validate_line(line)
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    return path


def main() -> None:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(output_dir)
    # Read-back gate: the file on disk must be byte-identical to the
    # winning line we validated, with no trailing newline added.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    assert written == WINNING_LINE, (
        "entry.txt does not match the winning line: %r" % written
    )
    print("wrote %s (%d characters)" % (path, len(WINNING_LINE)))


if __name__ == "__main__":
    main()
