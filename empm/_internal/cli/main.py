import typer
from typing_extensions import Annotated

from empm._internal.command.add import add_command
from empm._internal.command.install import install_command
from empm._internal.command.remove import remove_command
from empm._internal.command.home import home_command

app = typer.Typer()


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
    pack_url: str,
    pack_type: Annotated[
        bool, typer.Option(help="True: download release False: download repo")
    ] = False,
    pack_version: Annotated[str, typer.Option(help="pack version")] = None,
):
    add_command(pack_name, pack_url, pack_type, pack_version)


@app.command(help="remove a dependency from toml file")
def remove(pack_name: str):
    remove_command(pack_name)


@app.command(help="web GUI")
def home():
    home_command()
