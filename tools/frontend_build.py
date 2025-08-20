from __future__ import annotations

import os
import subprocess
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    """
    构建前执行前端构建：
    - EMPM_SKIP_FRONTEND_BUILD=1 可跳过
    - EMPM_PM 可指定包管理器：pnpm/yarn/npm（默认 yarn）
    """

    def initialize(self, version: str, build_data: dict) -> None:
        if os.environ.get("EMPM_SKIP_FRONTEND_BUILD") == "1":
            return

        root = Path(self.root) / "src"

        # 如果是从 sdist 解包目录构建（根目录含 PKG-INFO），跳过二次前端构建
        if (root / "PKG-INFO").exists():
            print(
                "[empm] detected sdist extraction context, skip frontend build for wheel."
            )
            return

        fe_dir = root / "empm" / "web" / "frontend"
        if not (fe_dir / "package.json").exists():
            return

        pm = os.environ.get("EMPM_PM", "yarn").lower()

        # 确保安装 devDependencies（避免生产模式跳过）
        env = os.environ.copy()
        env["YARN_PRODUCTION"] = "false"
        env.pop("NODE_ENV", None)

        if pm == "pnpm":
            install_cmd = [pm, "install", "--frozen-lockfile", "--prod=false"]
            build_cmd = [pm, "build"]
        elif pm == "yarn":
            install_cmd = [pm, "install", "--frozen-lockfile"]
            build_cmd = [pm, "build"]
        else:  # npm
            install_cmd = (
                ["npm", "ci", "--include=dev"]
                if (fe_dir / "package-lock.json").exists()
                else ["npm", "install", "--include=dev"]
            )
            build_cmd = ["npm", "run", "build"]

        print(f"[empm] frontend: {fe_dir}")
        print(f"[empm] running: {' '.join(install_cmd)}")
        subprocess.run(
            install_cmd, cwd=fe_dir, check=True, shell=(os.name == "nt"), env=env
        )

        print(f"[empm] running: {' '.join(build_cmd)}")
        subprocess.run(
            build_cmd, cwd=fe_dir, check=True, shell=(os.name == "nt"), env=env
        )

        if not (fe_dir / "dist").exists():
            print("[empm] 警告：未找到 frontend/dist，请确认前端构建脚本输出到该目录。")
