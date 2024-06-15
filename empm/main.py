import logging
import sys
from pathlib import Path

import typer
import uvicorn
from typing_extensions import Annotated

from web.main import web_app

from .utility import (
    Pack,
    TomlDepend,
)

log = logging.getLogger("rich")

app = typer.Typer()


@app.command()
def install():
    cfg = TomlDepend()

    depend_lib = cfg.get_depend()

    log.debug(f"depend_lib: {depend_lib}")

    for depend in depend_lib:
        log.debug(f"depend: {type(depend)}")
        if Path(f"lib/{depend}").exists():
            log.info(f"{depend}: {depend_lib[depend]}")
            continue

        try:
            log.debug(f"version: {depend_lib[depend]['version']}")
            pack = Pack(
                depend,
                depend_lib[depend]["url"],
                version=depend_lib[depend]["version"],
            )
        except KeyError:
            pack = Pack(depend, depend_lib[depend]["url"])
        pack.install()


@app.command()
def add(
    pack_name: str,
    pack_url: str,
    pack_type: Annotated[
        bool, typer.Option(help="True: download release False: download repo")
    ] = False,
    pack_version: Annotated[str, typer.Option(help="pack version")] = None,
):
    if pack_type:
        if pack_version is None:
            log.error("Unspecified release version!")
            sys.exit(1)

    toml_depend = TomlDepend()
    log.info("write toml file...")
    if pack_type:
        toml_depend.set_depend(pack_name, pack_url, pack_version)
    else:
        toml_depend.set_depend(pack_name, pack_url)

    log.info("install pack")
    if pack_type:
        pack = Pack(pack_name, pack_url, version=pack_version)
    else:
        pack = Pack(pack_name, pack_url, version=pack_version)
    pack.install()


@app.command()
def remove(pack_name: str):
    log.debug("run command 'remove'...")
    log.info(f"remove {pack_name}")
    pack_path = Path(f"lib/{pack_name}")
    pack_toml = TomlDepend()

    if pack_name in pack_toml.get_depend():
        pack_toml.delete_depend(pack_name)
        if pack_path.exists():
            log.debug(f"delete {pack_name}")
            Pack.delete(pack_path)
    else:
        log.error("not pack!")
        sys.exit(1)


@app.command()
def home():
    try:
        config = uvicorn.Config(web_app, port=5000, log_level="info", reload=True)
        server = uvicorn.Server(config)
        server.run()
    except KeyboardInterrupt:
        log.info("exit")
        sys.exit(1)
    except Exception as e:
        log.error(f"error: {e}")


def run():
    app()
