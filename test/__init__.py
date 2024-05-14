import logging
from logging.handlers import RotatingFileHandler
import cepack

log = logging.getLogger("rich")
log.setLevel(logging.DEBUG)

log_handle = RotatingFileHandler("debug.log", mode="w", backupCount=5, encoding="utf-8")
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)-8s - %(name)s - %(funcName)s - %(message)s "
)
log_handle.setFormatter(formatter)

log.addHandler(log_handle)

import os
os.makedirs('lib', exist_ok=True)
