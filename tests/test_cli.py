import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC = PROJECT_ROOT / "src"


def run_cli(*args: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONPATH": str(SRC)}
    return subprocess.run(
        [sys.executable, "-m", "toolkit", *args],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        env=env,
        check=False
    )

def test_cli_calc():
    res = run_cli("calc", "2+3*4")
    assert res.returncode == 0
    assert res.stdout.strip() == "14"


def test_cli_convert():
    res = run_cli("convert", "1", "--from", "kg", "--to", "g")

    assert res.returncode == 0
    assert res.stdout.strip() == "1000"


def test_cli_unknown_mode():
    res = run_cli("invalid_operation", "1")
    assert res.returncode == 2
    assert "Неизвестный режим" in res.stdout