"""Gate checks for the vending machine pickup line entry.

Mirrors the sealed scorer's gate: /output/entry.txt must be UTF-8 text
of 1 to 200 characters, not only white space. Also checks the line is
a single line and carries the machine's own world (coil / slot code).

Run: python3 tests/test_entry.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import LINE  # noqa: E402


def test_gate() -> None:
    assert isinstance(LINE, str)
    assert LINE.strip(), "line must not be only white space"
    assert 1 <= len(LINE) <= 200, f"length {len(LINE)} outside 1-200"
    assert "\n" not in LINE.strip(), "entry must be one line"
    LINE.encode("utf-8")  # must be valid UTF-8
    lowered = LINE.lower()
    assert "coil" in lowered, "line should draw on the machine's world"
    assert "a3" in lowered, "line should name a slot code"
    print(f"gate OK: {len(LINE)} chars, one line, UTF-8")


def test_program_output() -> None:
    import subprocess
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "entry.txt")
        env = dict(os.environ, ENTRY_OUTPUT=out)
        proc = subprocess.run(
            [sys.executable, "main.py"], cwd=os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))),
            env=env, capture_output=True, text=True)
        assert proc.returncode == 0, proc.stderr
        with open(out, encoding="utf-8") as f:
            written = f.read()
        assert written == LINE, "main.py output must equal the entry line"
        assert 1 <= len(written) <= 200
    print("program output OK: main.py writes the exact line")


if __name__ == "__main__":
    test_gate()
    test_program_output()
    print("ALL CHECKS PASSED")
