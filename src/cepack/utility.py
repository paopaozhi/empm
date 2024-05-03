import os
import sys
import shutil
from pathlib import Path
import re
import toml
import requests
import logging
from logging.handlers import RotatingFileHandler
# from git import Repo
# from git.exc import GitCommandError
from rich.logging import RichHandler
from rich import print
from rich import progress
from rich.progress import Progress
from rich.progress import TextColumn,TimeElapsedColumn,SpinnerColumn


FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

log_handle = RotatingFileHandler("build/lib/actions.log", mode="w", backupCount=5,encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)-8s - %(name)s - %(funcName)s - %(message)s ")
log_handle.setFormatter(formatter)

log.addHandler(log_handle)

cfg_file = toml.load("./depend.toml")

depend_lib = cfg_file["depend"]

def download_release(url,name,path=None):
    """下载release包到指定路径

    Args:
        url (str): release包链接
        name (str): 名称
        path (_type_, optional): 存放路径. Defaults to None.
    """
    headers = {'Accept-Encoding': 'identity'}
    ret = requests.get(url,stream=True,headers=headers)
    log.debug(ret.headers)

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        SpinnerColumn(),
        TimeElapsedColumn(),
    ) as progress:
        task1 = progress.add_task(f"[Download {name}..]")
        
        with open(f'build/lib/{name}.zip','wb') as fd:
            for data in ret.iter_content(chunk_size=128):
                fd.write(data)
                # fd.flush()

        log.debug("start unzip...")
        shutil.unpack_archive(f"build/lib/{name}.zip",f"build/lib/{name}", 'zip')
        log.debug("end unzip...")

    os.remove(f"build/lib/{name}.zip")  

        

def download_repo(url:str,name:str,path=None):
    """下载repo仓库到指定路径
    
    Args:
        url (str): 远程仓库链接
        name (str): 仓库名称
        path (_type_, optional): 存放路径. Defaults to None.
    """
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        SpinnerColumn(),
        TimeElapsedColumn(),
    ) as progress:
        task1 = progress.add_task(f"Download {name}...", total=len(depend_lib))

        download_path = Path(f"build/lib/{name}")  
        # os.path.join('build','lib',name)
        try:
            Repo.clone_from(url,to_path=download_path)
        except GitCommandError:
            pass
        progress.update(task1,advance=1)

def get_repo_info(url) -> dict:
    a = re.findall("/\w+",url)
    log.debug(f"findall_url:{a}")
    b = [i[1:] for i in a]
    c = {
        "owner" :b[1],
        "repo": b[2],
        "remote": b[0]
    }
    log.debug(f"info:{c}")
    return c

if __name__ == "__main__":
    base_url = "https://api.github.com"

    for lib_name in depend_lib:
        log.debug(lib_name)
        # 获取url
        lib_url = depend_lib[lib_name]["url"]

        lib_info =get_repo_info(lib_url)

        owner = lib_info["owner"]
        repo = lib_info["repo"]
        tag = depend_lib[lib_name]["version"]
        list_releases = base_url + f"/repos/{owner}/{repo}/releases/tags/{tag}"
        log.debug(f"list_releases: {list_releases}")

        ret = requests.get(list_releases)
        log.debug(ret.json())
        try:
            print(ret.json()["zipball_url"])
            release_url = ret.json()["zipball_url"]
            download_release(release_url,repo)
        except KeyError:
            download_repo(lib_url,repo)
