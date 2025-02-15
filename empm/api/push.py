import hashlib
import logging
import os
from pathlib import Path

import requests

log = logging.getLogger("rich")
g_gitea_packages_url = "https://git.aiotstudio.cn/api/packages/paopaozhi/generic"
token = os.environ.get("GITEA_TOKEN")


def push_sdk(name: str, version: str, path: Path):
    # 获取上传文件 mdk5
    with open(path, "rb") as f:
        byte = f.read()
        file_md5 = hashlib.md5(byte).hexdigest()

    # 上传软件包
    log.info(f"push pack {name} {version}")
    file_name = f"{name}_{version}.zip"
    r = requests.put(
        f"{g_gitea_packages_url}/{name}/{version}/{file_name}",
        headers={"Authorization": f"token {token}"},
        files={"file": open(path, "rb")},
    )
    log.debug(r.status_code)


def pull_sdk(name: str, version: str):
    package_get_url = f"https://git.aiotstudio.cn/api/v1/packages/paopaozhi/generic/{name}/{version}/files"
    download_path = Path(".empm/sdk")

    download_path.mkdir(parents=True, exist_ok=True)
    log.info(f"get sdk {name} {version}")

    # 获取文件名称
    r = requests.get(url=package_get_url,
                     headers={"Authorization": f"token {token}"})
    log.debug(r.status_code)
    package_json = r.json()
    log.debug(package_json)
    files_name = package_json[0]["name"]

    # 下载sdk
    r = requests.get(f"{g_gitea_packages_url}/{name}/{version}/{files_name}",
                     headers={"Authorization": f"token {token}"}, )
    log.debug(r.status_code)
    if r.status_code != 200:
        log.error(f"get sdk {name} {version} failed")
        log.error(r.text)
        return None

    # 写入至磁盘
    with open(f"{download_path}/{files_name}.zip", "wb") as f:
        f.write(r.content)


def parse_version(version_str):
    # 去掉前缀 'v'
    version_str = version_str.lstrip('v')

    # 主版本号是第一个字符
    major = version_str[0]
    # 修订版本号是最后一个字符
    patch = version_str[-1]
    # 次版本号是中间的部分
    minor = version_str[1:-1]

    parsed_version = f"v{major}.{minor}.{patch}"

    return parsed_version


def get_origin_info(name: str, version: str) -> dict:
    package_get_url = f"https://git.aiotstudio.cn/api/v1/packages/paopaozhi/generic/{name}/{version}/files"
    r = requests.get(url=package_get_url,
                     headers={"Authorization": f"token {token}"})
    if r.status_code != 200:
        return {"code": 0, "message": r.text}
    else:
        return {"code": -1, "message": r.text}


def push_sdk_latest():
    """
    STM32CUBE SDK上传至远端
    强依赖STM32CUBE_MX软件，需要提前下载包
    TODO: 解耦使其不依赖STM32CUBE_MX
    Returns:

    """
    log.info("push sdk latest")

    # 上传stm32cube sdk
    # 1. 获取stm32cube目录下所有已安装sdk包
    local_exist_str: list
    local_exist = dict()

    stm32cube_path = Path.home() / Path("STM32Cube/Repository")
    if not stm32cube_path.is_dir():
        log.error(f"get {stm32cube_path} failed")
        return None

    local_exist_str = list(stm32cube_path.glob("stm32*.zip"))
    log.info(local_exist_str)
    p: Path
    for p in local_exist_str:
        log.info(p.name)
        sdk_name = p.name.split("_")[2]
        sdk_version = parse_version(p.name.split("_")[3].split(".")[0])
        log.info(f"sdk name: {sdk_name} sdk version: {sdk_version}")

        local_exist_version = local_exist.get(sdk_name, {"version": "v0.0.0"}).get("version", "v0.0.0")
        if local_exist.get(sdk_name) is not None or local_exist_version < sdk_version:
            local_exist.update({sdk_name: {"version": sdk_version, "path": p}})

    # 2. 获取远程安装sdk包版本，对比版本上传
    for sdk_name in local_exist:
        sdk_item = local_exist[sdk_name]
        origin_name = f"STM32CUBE_{sdk_name.upper()}"

        package_get_url = f"https://git.aiotstudio.cn/api/v1/packages/paopaozhi/generic/{origin_name}/{sdk_item['version']}/files"
        r = requests.get(url=package_get_url,
                         headers={"Authorization": f"token {token}"})
        if r.status_code != 200:
            log.warning(f"get {package_get_url} failed")
            # 未获取到版本，上传新版本
            push_sdk(origin_name, sdk_item['version'], sdk_item.get("path"))


def push_lib_latest(name: str, version: str, lib_dir_path: Path = None):
    log.info("push command")

    # 1. 检查上传路径，版本
    lib_file_name = f"lib_{name}_{version}.zip"
    push_lib_dir_path = Path("dist")
    if not push_lib_dir_path.is_dir():
        raise Exception(f"get {push_lib_dir_path} failed")
    push_lib_path = push_lib_dir_path / Path(name)

    # 2. 比对远程库，名称，版本
    result = get_origin_info(name, version)
    if result == 0:
        log.warning("Already exist lib.")
        return None

    # 3. 上传lib包
    log.info(f"Push lib {name} {version}.")
    file_name = lib_file_name
    r = requests.put(
        f"{g_gitea_packages_url}/{name}/{version}/{file_name}",
        headers={"Authorization": f"token {token}"},
        files={"file": open(push_lib_path, "rb")},
    )
    log.debug(r.status_code)
    log.info("Push lib {name} {version} OK.")


if __name__ == "__main__":
    import empm

    push_sdk_latest()
