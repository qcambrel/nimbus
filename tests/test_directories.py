import os
from utils.constants import (
    ROOT_DIR, CACHE_DIR, TEMP_DIR, WEIGHTS_DIR
)

def test_project_root_dir():
    assert os.path.exists(ROOT_DIR)

    # These directories are nested in submodules
    assert os.path.exists(os.path.dirname(CACHE_DIR))
    assert os.path.exists(os.path.dirname(TEMP_DIR))
    assert os.path.exists(os.path.dirname(WEIGHTS_DIR))