import sys
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path
import os

web_app = FastAPI()

web_app.mount("/assets", StaticFiles(directory="web/html/dist/assets"), name="assets")


@web_app.get("/")
async def root():
    html_path = Path("web/html/dist/index.html")
    return FileResponse(html_path)


@web_app.get("/{whatever:path}")
async def get_static_files_or_404(whatever):
    html_path = Path("web/html/dist/index.html")
    # try open file for path
    file_path = os.path.join("web/html/dist", whatever)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse(html_path)


if __name__ == "__main__":
    try:
        uvicorn.run(web_app, port=5000, log_level="info")
    except KeyboardInterrupt:
        print("exit")
        sys.exit()
    except Exception as e:
        print(f"error: {e}")
