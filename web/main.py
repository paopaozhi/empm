from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from empm.utility import TomlDepend

web_app = FastAPI()

web_app.mount("/assets", StaticFiles(directory="web/html/dist/assets"), name="assets")


@web_app.get("/")
async def root():
    html_path = Path("web/html/dist/index.html")
    return FileResponse(html_path)


@web_app.get("/pack/info")
async def get_pack_info():
    cfg = TomlDepend()
    return cfg.info()


@web_app.get("/pack/dependencies")
async def get_pack_dependencies():
    cfg = TomlDepend()
    return cfg.get_depend()
