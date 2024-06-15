import os
import shutil
import subprocess
import unittest
from pathlib import Path

from empm.utility import download_release, download_repo

from .utility.env_manage import auto_clear_env


class TestUtility(unittest.TestCase):
    def test_downloadRepo(self):
        # clean env, delete file
        lib_path = Path("lib/ulog")

        if lib_path.exists():
            if os.name == "nt":
                subprocess.run(
                    ["rmdir", "/S", "/Q", lib_path],
                    shell=True,
                )
            elif os.name == "posix":
                shutil.rmtree(lib_path)

        download_repo("https://github.com/rdpoor/ulog", "ulog")

        ret = os.path.isdir(lib_path)
        self.assertEqual(True, ret)

    @auto_clear_env
    def test_downloadRelease(self):
        lib_path = Path("lib/gitmoji")
        download_release(
            "https://github.com/carloscuesta/gitmoji", name="gitmoji", version="v3.14.0"
        )

        ret = os.path.isdir(lib_path)
        assert ret is True

    def test_get_depend(slef):
        pass

    def test_set_depend(self):
        pass

    def test_delete_pack(self):
        from empm.utility import delete_pack

        pack_path = Path("lib/ulogs")

        os.makedirs("lib/ulogs", exist_ok=True)
        delete_pack(pack_path)

        assert Path("lib/ulogs").exists() is False
