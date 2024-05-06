import sys
import logging

sys.path.append(r"..\src")

from cepack.utility import download_repo

if __name__ == "__main__":
    log = logging.getLogger("rich")
    log.setLevel(logging.DEBUG)
    
    download_repo("https://gitee.com/brick-girl/brick-girl","brick-girl")
    # run()
    # home = Path.home()
    # print(home)