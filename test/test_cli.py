import os
import shutil
import subprocess
from pathlib import Path

import toml
from typer.testing import CliRunner

from empm._internal.cli.main import app
from test.utility import env_manage

from .utility import init_test_toml, log, write_test_toml

runner = CliRunner()
manage_file = Path("empm.toml")


def test_cli():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


@env_manage.auto_clear_env
def test_cli_install():
    cfg = """
    [dependencies]
    gitmoji = {url = "https://github.com/carloscuesta/gitmoji", version = "v3.14.0"}
    ulog = { url = "https://github.com/rdpoor/ulog"}
    """.replace(" ", "")

    write_test_toml(cfg)

    result = runner.invoke(app, ["install"])
    assert result.exit_code == 0

    lib1_path = Path("lib/gitmoji")
    lib2_path = Path("lib/ulog")
    ret1 = lib1_path.exists()
    ret2 = lib2_path.exists()

    assert ret1 is True
    assert ret2 is True


@env_manage.auto_clear_env
def test_cli_install_load_toml():
    result = runner.invoke(app, ["install"])
    assert result.exit_code != 0


def test_cli_install_exist_pack():
    cfg = """
    [dependencies]
    # gitmoji = {url = "https://github.com/carloscuesta/gitmoji", version = "v3.14.0"}
    ulog = { url = "https://github.com/rdpoor/ulog"}
    """.replace(" ", "")

    write_test_toml(cfg)

    pack1_path = Path("lib/ulog")
    os.makedirs(pack1_path, exist_ok=True)

    result = runner.invoke(app, ["install"])

    assert result.exit_code == 0


@env_manage.auto_clear_env
def test_cli_add_repo():
    init_test_toml()

    result = runner.invoke(app, ["add", "ulog", "https://github.com/rdpoor/ulog"])

    assert result.exit_code == 0

    cfg = toml.load(manage_file)

    assert "ulog" in cfg["dependencies"]

    lib_path = Path("lib/ulog")
    ret = os.path.isdir(lib_path)

    assert True is ret


@env_manage.auto_clear_env
def test_cli_add_release():
    init_test_toml()

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

    assert result.exit_code == 0

    cfg = toml.load(manage_file)

    assert "gitmoji" in cfg["dependencies"]

    lib_path = Path("lib/gitmoji")
    ret = lib_path.exists()

    assert True is ret


@env_manage.auto_clear_env
def test_cli_add_error():
    init_test_toml()

    result = runner.invoke(
        app, ["add", "ulog", "--pack-type", "https://github.com/rdpoor/ulog"]
    )
    assert result.exit_code != 0


@env_manage.auto_clear_env
def test_ci_remove():
    cfg = """
    [depend]
    gitmoji = {url = "https://github.com/carloscuesta/gitmoji", version = "v3.14.0"}
    ulog = { url = "https://github.com/rdpoor/ulog"}
    
    [dependencies]
    gitmoji = {url = "https://github.com/carloscuesta/gitmoji", version = "v3.14.0"}
    ulog = { url = "https://github.com/rdpoor/ulog"}
    """.replace(" ", "")

    write_test_toml(cfg)

    # 创建测试文件
    pack1_path = Path("lib/ulog")
    os.makedirs(pack1_path, exist_ok=True)

    result = runner.invoke(app, ["remove", "ulog"])

    assert result.exit_code == 0

    ret = pack1_path.exists()
    assert False is ret

    cfg = toml.load("empm.toml")
    assert "ulog" not in cfg["dependencies"]


@env_manage.auto_clear_env
def test_cli_remove_error():
    init_test_toml()
    result = runner.invoke(app, ["remove", "ulog"])
    assert result.exit_code == 1


def delete_folder(path: Path):
    if os.name == "nt":
        result = subprocess.run(
            ["rmdir", "/S", "/Q", path],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.stderr != b"":
            log.error(result.stderr.decode("GBK"))
    elif os.name == "posix":
        shutil.rmtree(path)


def test_cli_new():
    empm_path = Path.home() / ".empm"
    test_path = Path("test_stmf1")
    delete_folder(empm_path)

    result = runner.invoke(app, ["new", "test_stmf1"])
    assert result.exit_code == 0
    assert empm_path.exists()
    assert test_path.exists()

    result = runner.invoke(app, ["new", "test_stmf1"])
    assert empm_path.exists()

    delete_folder("test_stmf1")


@env_manage.auto_clear_env
def test_cli_home():
    pass
    # with pytest.raises(KeyboardInterrupt):
    #     result = runner.invoke(app, ["home"])
    #     assert result.exit_code != 0
