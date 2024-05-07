import sys
from pathlib import Path
import logging

sys.path.append(r"..\src")

from cepack.main import run

if __name__ == "__main__":
    log = logging.getLogger("rich")
    log.setLevel(logging.DEBUG)
    
    run()
    # home = Path.home()
    # print(home)