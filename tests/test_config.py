from core.config import config, BASE_DIR
from pathlib import Path
import pytest

# check if config correctly identifies the root directory
def test_base_dir():
    assert BASE_DIR.name == "todo"
