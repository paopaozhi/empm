import typer
import logging
import toml
from .utility import download_release,get_repo_info
import requests
import sys

log = logging.getLogger("rich")
log.setLevel(logging.INFO)

app = typer.Typer()

@app.callback(invoke_without_command=True)
def install():
    base_url = "https://api.github.com"
    
    try:
        cfg_file = toml.load("./depend.toml")
    except:
        log.error("none depend.toml!")
        sys.exit()

    depend_lib = cfg_file["depend"]
    
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
        try:
            # print(ret.json()["zipball_url"])
            release_url = ret.json()["zipball_url"]
            download_release(release_url,repo)
        except KeyError:
            pass
    
@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")
      
@app.command()
def init():
    print("default")
        
def run():
    app()
    
if __name__ == "__main__":
    run()