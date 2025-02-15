import logging
from pathlib import Path

from empm.utility import Pack, TomlDepend

log = logging.getLogger("rich")


def install_command():
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