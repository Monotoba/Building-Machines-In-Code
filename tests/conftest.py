"""Test configuration for the standalone Part 9 modules."""

import sys
from pathlib import Path


PART_9 = Path(__file__).resolve().parents[1] / "part-9"
sys.path.insert(0, str(PART_9))
