import typer
from typing_extensions import Annotated, Optional
import logging

from ..api.add import add_command
from ..api.home import home_command
from ..api.install import install_command
from ..api.new import new_command
from ..api.push import push_sdk_latest, pull_sdk
from ..api.remove import remove_command

app = typer.Typer()
log = logging.getLogger('rich')


@app.command(
    help="install all dependencies from toml file",
)
def install():
    install_command()


@app.command(
    help="add a new dependency to toml file",
)
def add(
        pack_name: str,
        pack_url: Annotated[str, typer.Argument(help="pack url")] = None,
        pack_version: Annotated[str, typer.Argument(help="pack version")] = None,
        pack_type: Annotated[
            bool, typer.Option(help="True: download release False: download repo")
        ] = False,
        install_type: Annotated[str, typer.Option(help="install sdk or library")] = "lib"
):
    if install_type == "lib":
        add_command(pack_name, pack_url, pack_type, pack_version)
    elif install_type == "sdk":
        pull_sdk(pack_name, pack_version)
    else:
        log.error("Unknown install type")


@app.command(help="remove a dependency from toml file")
def remove(pack_name: str):
    remove_command(pack_name)


@app.command(help="new project")
def new(project_name: Annotated[str, typer.Argument(help="project name")]):
    new_command(project_name)


@app.command(help="web GUI")
def home():
    home_command()


@app.command(help="push pack")
def push(push_type: Annotated[str, typer.Option(help="pack type")]):
    if push_type == "sdk":
        push_sdk_latest()
    elif push_type == "lib":
        pass
