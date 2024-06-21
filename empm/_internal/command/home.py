import logging
import sys

import uvicorn

from empm._internal.web.main import web_app


log = logging.getLogger("rich")


def home_command():
    try:
        config = uvicorn.Config(web_app, port=5000, log_level="info", reload=True)
        server = uvicorn.Server(config)
        server.run()
    except KeyboardInterrupt:
        log.info("exit")
        sys.exit(1)
    except Exception as e:
        log.error(f"error: {e}")
