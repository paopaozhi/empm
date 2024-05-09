import typer
import logging
import toml
from .utility import download_repo, download_release, get_repo_info
import requests
import sys
from pathlib import Path

log = logging.getLogger("rich")

app = typer.Typer()


@app.command()
def install():
    base_url = "https://api.github.com"

    try:
        cfg_file = toml.load("./depend.toml")
    except:
        log.error("none depend.toml!")
        sys.exit()

    depend_lib = cfg_file["depend"]

    for lib_name in depend_lib:
        if Path(f"lib/{lib_name}").exists():
            log.info(f"{lib_name}: {depend_lib[lib_name]}")
            continue

        log.debug(lib_name)
        # 获取url
        lib_url = depend_lib[lib_name]["url"]

        lib_info = get_repo_info(lib_url)

        owner = lib_info["owner"]
        repo = lib_info["repo"]
        tag = depend_lib[lib_name]["version"]
        list_releases = base_url + f"/repos/{owner}/{repo}/releases/tags/{tag}"
        log.debug(f"list_releases: {list_releases}")

        ret = requests.get(list_releases)
        try:
            # print(ret.json()["zipball_url"])
            release_url = ret.json()["zipball_url"]
            download_release(release_url, repo)
        except KeyError:
            download_repo(lib_url, repo)


@app.command()
def add(
    pack_name: str,
    pack_type: bool = False,
    pack_url: str = "",
    pack_version: str = "",
):
    pass


@app.command()
def init():
    print("default")


def run():
    app()


if __name__ == "__main__":
    run()
