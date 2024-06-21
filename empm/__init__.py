import logging

from rich.logging import RichHandler

__version__ = "0.0.9"

FORMAT = "%(message)s"
logging.basicConfig(format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

log = logging.getLogger("rich")
log.setLevel(logging.INFO)
