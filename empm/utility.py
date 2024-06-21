import logging
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

import requests
import toml
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

log = logging.getLogger("rich")


def download_release(url, name, version, path=None):
    """下载release包到指定路径

    Args:
        url (str): release包仓库链接
        name (str): 名称
        path (_type_, optional): 存放路径. Defaults to None.

    Raises:
        FileExistsError: If the destination folder already exists.
        PermissionError: If there is a permission error while moving the folder.

    Returns:
        None

    """
    if path is None:
        path = Path("lib/")
    else:
        path = Path(path)

    download_path = Path(path, f"{name}.zip")
    log.debug("download pack path: " + str(download_path))

    target_path = Path("lib/")

    if Path(f"lib/{name}").exists():
        log.info(f"{name}: pack already exists")

    log.debug(name)
    # 获取url
    pack_info = get_repo_info(url)
    owner = pack_info["owner"]
    repo = pack_info["repo"]
    tag = version

    base_url = "https://api.github.com"
    get_releases_url = base_url + f"/repos/{owner}/{repo}/releases/tags/{tag}"
    log.debug(f"releases url: {get_releases_url}")

    ret = requests.get(get_releases_url)
    release_url = ret.json()["zipball_url"]
    log.debug(f"release_download_url: {release_url}")

    headers = {"Accept-Encoding": "identity"}
    ret = requests.get(release_url, stream=True, headers=headers)

    log.info(f"download pack {name}...")
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        SpinnerColumn(),
        TimeElapsedColumn(),
    ) as progress:
        progress.add_task(f"[Download {name}..]")

        with download_path.open("wb") as fd:
            for data in ret.iter_content(chunk_size=128):
                fd.write(data)
                # fd.flush()

        log.debug(f"start decompressing {name}...")
        shutil.unpack_archive(download_path, target_path, format="zip")
        log.debug(f"complete decompressing {name}...")

    # 重命名文件夹
    with ZipFile(download_path, "r") as zip_ref:
        log.debug("zip file name: " + zip_ref.namelist()[0])
        filenameDir_path = Path("lib/", zip_ref.namelist()[0])
        log.debug(filenameDir_path)
    try:
        shutil.move(filenameDir_path, f"lib/{name}")
    except FileExistsError:
        shutil.rmtree(f"lib/{name}")
        shutil.move(filenameDir_path, f"lib/{name}")
    except PermissionError as e:
        log.error(f"权限错误：{e}")
    # 删除包
    os.remove(download_path)


def download_repo(url: str, name: str, path=None):
    """下载repo仓库到指定路径

    Args:
        url (str): 远程仓库链接
        name (str): 仓库名称
        path (_type_, optional): 存放路径. Defaults to None.

    Returns:
        None
    """
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        SpinnerColumn(),
        TimeElapsedColumn(),
    ) as progress:
        progress.add_task(f"Download {name}...")

        download_path = Path(f"lib/{name}")
        log.debug(download_path)

        result = subprocess.run(
            ["git", "clone", url, download_path],
            shell=True,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        if result.stdout != b"":
            log.info(result.stdout.decode("utf-8"))

        if result.stderr != b"":
            log.error(result.stderr.decode("utf-8"))


def get_repo_info(url: str) -> dict:
    """Get repository information from a given URL.

    Args:
        url (str): The URL of the repository.

    Returns:
        dict: A dictionary containing the owner, repo, and remote information of the repository.
    """
    a = re.findall("/\w+", url)
    log.debug(f"findall_url:{a}")
    b = [i[1:] for i in a]
    c = {"owner": b[1], "repo": b[2], "remote": b[0]}
    log.debug(f"info:{c}")
    return c


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


class Pack:
    def __init__(self, name: str, url: str, version=None, path=None):
        self.name = name
        self.url = url
        self.version = version
        if path is None:
            self.path = Path("lib/")
        else:
            self.path = path

    def __download(self, pack_type="repo"):
        if pack_type == "repo":
            download_repo(self.url, self.name, self.path)
        elif pack_type == "release":
            download_release(self.url, self.name, self.version, self.path)

    def install(self):
        if self.version is None:
            self.__download()
        else:
            self.__download(pack_type="release")

    def add(self, url, name, version=None, pack_type="repo"):
        self.__download(url, name, version, pack_type=pack_type)

    def delete(path: Path):
        delete_folder(path)


class TomlDepend:
    def __init__(self) -> None:
        try:
            self._cfg_file = toml.load("empm.toml")
        except Exception:
            log.error("none empm.toml!")
            sys.exit(1)

    def info(self):
        return self._cfg_file.get("package", {})

    def get_depend(self) -> dict:
        return self._cfg_file.get("dependencies", {})

    def set_depend(self, name: str, url: str, version=None):
        log.info(f"Wire {name} to empm.toml")
        depend_lib = self.get_depend()
        if version is None:
            depend_lib[name] = {"url": url}
        else:
            depend_lib[name] = {"url": url, "version": version}

        self._cfg_file["dependencies"] = depend_lib
        log.debug(f"{name}: {self._cfg_file['dependencies'][name]}")

        with open(Path("empm.toml"), "w+") as fd:
            d = toml.dump(self._cfg_file, fd)
            log.debug(d)

    def delete_depend(self, name: str):
        log.debug(f"Delete {name} from toml")
        self.get_depend().pop(name)
        with open(Path("empm.toml"), "w+") as fd:
            d = toml.dump(self._cfg_file, fd)
            log.debug(d)
