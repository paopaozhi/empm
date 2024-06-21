from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from empm.utility import TomlDepend

web_app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

web_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base_path = Path(Path(__file__).parent, "html/dist")

web_app.mount("/assets", StaticFiles(directory=f"{base_path}/assets"), name="assets")


@web_app.get("/")
async def root():
    html_path = Path(base_path, "index.html")
    return FileResponse(html_path)


@web_app.get("/pack/info")
async def get_pack_info():
    cfg = TomlDepend()
    return cfg.info()


@web_app.get("/pack/dependencies")
async def get_pack_dependencies():
    cfg = TomlDepend()
    dependencies = cfg.get_depend()
    depend = []
    for i in dependencies:
        try:
            depend.append(
                {
                    "name": i,
                    "url": dependencies[i]["url"],
                    "version": dependencies[i]["version"],
                }
            )
        except Exception:
            depend.append({"name": i, "url": dependencies[i]["url"], "version": None})

    return depend
