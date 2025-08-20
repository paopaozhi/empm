import logging
import sys

import typer
from typing_extensions import Annotated

from empm.utility import Pack, TomlDepend

log = logging.getLogger("rich")


def add_command(
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
