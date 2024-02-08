from fastapi.testclient import TestClient


def test_hello_world(client: TestClient):
    r = client.get("/hello-world")
    data = r.json()

    assert r.status_code == 200
    assert data == "hello world"
