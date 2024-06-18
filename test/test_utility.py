import os
from pathlib import Path

from .utility.env_manage import auto_clear_env


def test_get_depend():
    pass


def test_set_depend():
    pass


@auto_clear_env
def test_delete_folder():
    from empm.utility import delete_folder

    pack_path = Path("lib/ulogs")

    os.makedirs(pack_path, exist_ok=True)
    delete_folder(pack_path)

    assert Path(pack_path).exists() is False


@auto_clear_env
def test_delete_folder_error():
    from empm.utility import delete_folder

    pack_path = Path("lib/ulogs")

    delete_folder(pack_path)

    assert Path(pack_path).exists() is False
