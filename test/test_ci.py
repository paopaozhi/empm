import os
from pathlib import Path
import shutil
import subprocess
import unittest
from typer.testing import CliRunner

from cepack.main import app
from . import *

runner = CliRunner()

class TestCi(unittest.TestCase):
    def test_ci_install(self):
        
        # clean env, delete file
        lib_path = Path("lib")
        lib_dir = os.listdir(lib_path)
        
        if os.name == "nt":
            for lib in lib_dir:
                if Path(lib).exists():
                    subprocess.run(["rmdir","/S","/Q",lib],shell=True)
        elif os.name == "posix":
            for lib in lib_dir:
                shutil.rmtree(lib)
            
        log.info("TestCi Start")
        result = runner.invoke(app,["install"])
        print(result.stdout)
        
        lib1_path = Path("lib/gitmoji")
        lib2_path = Path("lib/ulog")
        ret1 = os.path.isdir(lib1_path)
        ret2 = os.path.isdir(lib2_path)
        
        self.assertEqual(True,ret1)
        self.assertEqual(True,ret2)
        log.info("TestCi End")
        