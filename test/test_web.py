from fastapi.testclient import TestClient
from web.main import web_app

client = TestClient(web_app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

    response = client.get("/vite.svg")
    assert response.status_code == 200

    response = client.get("/index")
    assert response.status_code == 200
