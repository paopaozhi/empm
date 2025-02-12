import logging
import os
import shutil
from logging.handlers import RotatingFileHandler
from pathlib import Path

import empm  # noqa: F401

log = logging.getLogger("rich")
log.setLevel(logging.DEBUG)

log_handle = RotatingFileHandler("debug.log", mode="w", backupCount=5, encoding="utf-8")
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)-8s - %(name)s - %(filename)s:%(funcName)s - %(message)s "
)
log_handle.setFormatter(formatter)

log.addHandler(log_handle)


os.makedirs("lib", exist_ok=True)

test_workdir_path = Path("test_workdir")
shutil.rmtree(test_workdir_path, ignore_errors=True)
test_workdir_path.mkdir(parents=True, exist_ok=True)
os.chdir(test_workdir_path)
