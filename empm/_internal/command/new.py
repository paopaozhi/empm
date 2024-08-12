import logging
import os
import shutil
import subprocess
from pathlib import Path

import typer
from typing_extensions import Annotated

log = logging.getLogger("rich")
g_base_example_url = "https://github.com/paopaozhi/embedded-example-"


def new_command(
    project_name: str,
    project_board: Annotated[
        str, typer.Option(help="project board. eg:stmf1 stm32f4 stm32h7")
    ] = "stmf1",
):
    old_path = Path.cwd()
    empm_path = Path.home() / ".empm"

    if not os.path.exists(empm_path):
        os.mkdir(empm_path)

    if not os.path.exists(empm_path / f"embedded-example-{project_board}"):
        os.chdir(empm_path)
        result = subprocess.run(
            f"git clone {g_base_example_url}{project_board}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        result.check_returncode()
        os.chdir(old_path)

    if not os.path.exists(old_path / project_name):
        shutil.copytree(empm_path / f"embedded-example-{project_board}", project_name)
    else:
        log.warning(f"{project_name} already exists")
