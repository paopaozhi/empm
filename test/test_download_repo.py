import os
from pathlib import Path
import logging
import shutil
import subprocess
import unittest

from cepack.utility import download_repo

class TestDownloadRepo(unittest.TestCase):
    def test_init(self):
        lib_path=Path("lib/brick-girl")
        if os.name == "nt":
            subprocess.run(["rmdir","/S","/Q",lib_path],shell=True,);
        elif os.name == "posix":
            shutil.rmtree(lib_path)
        if os.path.isdir(lib_path):
            shutil.rmtree(lib_path)
        download_repo("https://gitee.com/brick-girl/brick-girl","brick-girl")
        
        ret = os.path.isdir(lib_path)
        self.assertEqual(True,ret)
