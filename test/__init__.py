import logging
import os
from logging.handlers import RotatingFileHandler

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
