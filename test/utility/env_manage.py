import os
import shutil
from pathlib import Path
import subprocess

from . import log


def _clear_lib_dir():
    """
    清理lib文件夹
    """
    lib_path = Path("lib")
    lib_dir = os.listdir(lib_path)
    log.debug(f"lib_dir: {lib_dir}")

    for folder in os.listdir(lib_path):
        # 检查这个条目是否是一个文件夹
        if os.path.isdir(os.path.join(lib_path, folder)):
            _libpath = Path(lib_path, folder)
            log.debug(f"delete {_libpath}")
            if os.name == "nt":
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
                shutil.rmtree(_libpath)
    # init
    if Path("empm.toml").exists():
        os.remove("empm.toml")


def auto_clear_env(callback):
    def wrap_the_function(*args, **kwargs):
        _clear_lib_dir()
        callback(*args, **kwargs)
        _clear_lib_dir()

    return wrap_the_function
