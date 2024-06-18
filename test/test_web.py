from fastapi.testclient import TestClient

from empm._internal.web.main import web_app
from test.utility import env_manage

from .utility import write_test_toml

client = TestClient(web_app)


@env_manage.auto_clear_env
def test_read_main():
    testConfig = """
    [package]
    name = "empm"
    version = "0.1.0"
    authors = ["paopaozhi"]

    [dependencies]
    gitmoji = { url = "https://github.com/carloscuesta/gitmoji", version = "v3.14.0" }
    ulog = { url = "https://github.com/rdpoor/ulog" }
    """

    write_test_toml(testConfig)

    response = client.get("/")
    assert response.status_code == 200

    response = client.get("/pack/info")
    assert response.status_code == 200

    response = client.get("/pack/dependencies")
    assert response.status_code == 200
