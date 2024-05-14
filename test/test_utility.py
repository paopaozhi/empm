import os
from pathlib import Path
import logging
import shutil
import subprocess
import unittest

from cepack.utility import download_repo


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
        
    def test_get_depend(slef):
        pass
    
    def test_set_depend(self):
        pass
