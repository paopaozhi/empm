import toml
from fastapi.testclient import TestClient

from test.utility import env_manage
from web.main import web_app

client = TestClient(web_app)

@env_manage.auto_clear_env
def test_read_main():
    empm_cfg = """
    [package]
    name = "empm"
    version = "0.1.0"
    authors = ["paopaozhi"]

    [dependencies]
    gitmoji = { url = "https://github.com/carloscuesta/gitmoji", version = "v3.14.0" }
    ulog = { url = "https://github.com/rdpoor/ulog" }
    """

    cfg_class = {}
    cfg_class = toml.loads(empm_cfg)

    with open("empm.toml", "w") as fd:
        if cfg_class:
            toml.dump(cfg_class, fd)

    response = client.get("/")
    assert response.status_code == 200

    response = client.get("/pack/info")
    assert response.status_code == 200

    response = client.get("/pack/dependencies")
    assert response.status_code == 200
