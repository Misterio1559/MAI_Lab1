from pathlib import Path
from sys import path

SRC = Path(__file__).resolve().parent.parent / "src"
path.insert(0, str(SRC))