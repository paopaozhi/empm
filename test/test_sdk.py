from empm._internal.command.push import push_sdk, pull_sdk
from pathlib import Path

def test_push_sdk():
    test_push_sdk_path = Path().home() / Path("STM32Cube/Repository/stm32cube_fw_l4_v1181.zip")
    push_sdk("STM32CUBE_L4", "v1.18.1", test_push_sdk_path)


def test_pull_sdk():
    pull_sdk("STM32CUBE_L4", "v1.18.1")
