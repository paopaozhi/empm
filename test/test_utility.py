import os
from pathlib import Path


def test_get_depend():
    pass


def test_set_depend():
    pass


def test_delete_pack():
    from empm.utility import delete_pack

    pack_path = Path("lib/ulogs")

    os.makedirs("lib/ulogs", exist_ok=True)
    delete_pack(pack_path)

    assert Path("lib/ulogs").exists() is False
