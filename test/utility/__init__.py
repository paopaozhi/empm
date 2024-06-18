import logging

import toml

log = logging.getLogger("rich")
log.setLevel(logging.DEBUG)


def write_test_toml(content: str, manage_file="empm.toml"):
    cfg_class = {}
    try:
        cfg_class = toml.loads(content)
    except toml.TomlDecodeError:
        log.error(f"content: \n{content}")
        log.error("toml decode error")

    with open(manage_file, "w") as fd:
        if cfg_class:
            toml.dump(cfg_class, fd)


def init_test_toml(manage_file="empm.toml"):
    with open(manage_file, "w") as fd:
        fd.write("# Test command")
        fd.flush()
