import os
import subprocess
import unittest
from pathlib import Path
from test import log
from test.utility import env_manage

import toml
from typer.testing import CliRunner

from empm.main import app

runner = CliRunner()


class TestCi(unittest.TestCase):
    def test_ci_main(self):
        result = subprocess.run(
            ["python", "-m", "empm", "--help"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        result.check_returncode()

    @env_manage.auto_clear_env
    def test_ci_install(self):
        cfg = """
        [depend]
        gitmoji = {url = "https://github.com/carloscuesta/gitmoji", version = "v3.14.0"}
        ulog = { url = "https://github.com/rdpoor/ulog" }
        
        [dependencies]
        gitmoji = {url = "https://github.com/carloscuesta/gitmoji", version = "v3.14.0"}
        ulog = { url = "https://github.com/rdpoor/ulog" }
        """.replace(" ", "")

        cfg_class = {}
        cfg_class = toml.loads(cfg)

        log.debug(f"cfg_class: {cfg_class}")

        with open("empm.toml", "w") as fd:
            fd.write("# Test command install")
            fd.flush()
        with open("empm.toml", "w") as fd:
            if cfg_class:
                toml.dump(cfg_class, fd)

        log.info("TestCi Start")
        result = runner.invoke(app, ["install"])
        print(result.stdout)
        assert result.exit_code == 0

        lib1_path = Path("lib/gitmoji")
        lib2_path = Path("lib/ulog")
        ret1 = os.path.isdir(lib1_path)
        ret2 = os.path.isdir(lib2_path)

        self.assertEqual(True, ret1)
        self.assertEqual(True, ret2)
        log.info("TestCi End")

    @env_manage.auto_clear_env
    def test_ci_install_load_toml(self):
        result = runner.invoke(app, ["install"])
        assert result.exit_code != 0

    @env_manage.auto_clear_env
    def test_ci_add(self):
        with open("empm.toml", "w") as fd:
            fd.write("# Test command add")

        log.info("Test command add")
        runner.invoke(
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
        runner.invoke(app, ["add", "ulog", "https://github.com/rdpoor/ulog"])

        cfg = toml.load("empm.toml")
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

        result = runner.invoke(
            app, ["add", "ulog", "--pack-type", "https://github.com/rdpoor/ulog"]
        )
        assert result.exit_code != 0

    @env_manage.auto_clear_env
    def test_ci_remove(self):
        cfg = """
        [depend]
        gitmoji = {url = "https://github.com/carloscuesta/gitmoji", version = "v3.14.0"}
        ulog = { url = "https://github.com/rdpoor/ulog"}
        
        [dependencies]
        gitmoji = {url = "https://github.com/carloscuesta/gitmoji", version = "v3.14.0"}
        ulog = { url = "https://github.com/rdpoor/ulog"}
        """.replace(" ", "")

        cfg_class = {}
        cfg_class = toml.loads(cfg)

        with open("empm.toml", "w") as fd:
            fd.write("# Test command remove")
            fd.flush()
        with open("empm.toml", "w") as fd:
            if cfg_class:
                toml.dump(cfg_class, fd)

        # 创建测试文件
        pack1_path = Path("lib/ulog")
        os.makedirs(pack1_path, exist_ok=True)

        result = runner.invoke(app, ["remove", "ulog"])

        assert result.exit_code == 0

        ret = pack1_path.exists()
        self.assertEqual(False, ret)
        cfg = toml.load("empm.toml")
        self.assertNotIn("ulog", cfg["depend"])

        result = runner.invoke(app, ["remove", "not-ulog"])
        assert result.exit_code != 0

    @env_manage.auto_clear_env
    def test_ci_home(self):
        pass
        # with pytest.raises(KeyboardInterrupt):
        #     result = runner.invoke(app, ["home"])
        #     assert result.exit_code != 0
