import os
import sys
from pathlib import Path
import shutil
import subprocess
import unittest

import toml
from typer.testing import CliRunner

from cepack.main import app
from test.utility import env_manage
from test import log

runner = CliRunner()


class TestCi(unittest.TestCase):
    @env_manage.auto_clear_env
    def test_ci_install(self):

        cfg = """
        [package]
        name = "cepack_test"
        version = "0.0.2"
        authors = ["泡泡纸 <paopaozhi@hotmail.com>"]
        
        [depend]
        gitmoji = {url = "https://github.com/carloscuesta/gitmoji", version = "v3.14.0"}
        ulog = { url = "https://github.com/rdpoor/ulog", version = "0.0.1" }
        
        [dependencies]
        gitmoji = {url = "https://github.com/carloscuesta/gitmoji", version = "v3.14.0"}
        ulog = { url = "https://github.com/rdpoor/ulog", version = "0.0.1" }
        """.replace(
            " ", ""
        )

        cfg_class = {}
        cfg_class = toml.loads(cfg)
        
        log.debug(f"cfg_class: {cfg_class}")

        with open("depend.toml", "w") as fd:
            fd.write("# Test command install")
            fd.flush()
            if cfg_class:
                toml.dump(cfg_class, fd)

        # clean env, delete file
        lib_path = Path("lib")
        lib_dir = os.listdir(lib_path)
        print(lib_dir)

        if os.name == "nt":
            for lib in lib_dir:
                _libpath = Path(lib_path, lib)
                if _libpath.exists():
                    log.debug(f"delete {_libpath}")
                    result = subprocess.run(
                        ["rmdir", "/S", "/Q", _libpath],
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    if result.stdout != b"":
                        log.info(result.stdout.decode("GBK"))
                    if result.stderr != b"":
                        log.error(result.stderr.decode("GBK"))
        elif os.name == "posix":
            for lib in lib_dir:
                shutil.rmtree(lib)

        log.info("TestCi Start")
        result = runner.invoke(app, ["install"])

        lib1_path = Path("lib/gitmoji")
        lib2_path = Path("lib/ulog")
        ret1 = os.path.isdir(lib1_path)
        ret2 = os.path.isdir(lib2_path)

        self.assertEqual(True, ret1)
        self.assertEqual(True, ret2)
        log.info("TestCi End")

    @env_manage.auto_clear_env
    def test_ci_add(self):
        with open("depend.toml", "w") as fd:
            fd.write("# Test command add")

        log.info("Test command add")
        result = runner.invoke(
            app,
            [
                "add",
                "--pack-type",
                "--pack-version",
                "v3.14.0",
                "gitmoji",
                "https://github.com/carloscuesta/gitmoji",
            ],
        )
        # assert result.exit_code != 0
        result = runner.invoke(app, ["add", "ulog", "https://github.com/rdpoor/ulog"])

        cfg = toml.load("depend.toml")
        log.info("test ulog")
        self.assertIn("ulog", cfg["depend"])
        log.info("test gitmoji")
        self.assertIn("gitmoji", cfg["depend"])

        lib1_path = Path("lib/gitmoji")
        lib2_path = Path("lib/ulog")
        ret1 = os.path.isdir(lib1_path)
        ret2 = os.path.isdir(lib2_path)

        self.assertEqual(True, ret1)
        self.assertEqual(True, ret2)
