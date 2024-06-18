from pathlib import Path
import sys

from empm.utility import Pack, TomlDepend
import logging

log = logging.getLogger("rich")


def remove_command(pack_name: str):
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
