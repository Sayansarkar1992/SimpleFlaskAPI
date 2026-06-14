import pytest

from src.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_health_api(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "service": "simple-flask-api"}


def test_greet_api_with_name(client):
    response = client.get("/api/greet?name=Sayan")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello, Sayan!"}


def test_greet_api_defaults_to_world(client):
    response = client.get("/api/greet")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello, World!"}


def test_add_api(client):
    response = client.post("/api/add", json={"a": 7, "b": 5})

    assert response.status_code == 200
    assert response.get_json() == {"a": 7, "b": 5, "result": 12}


def test_add_api_rejects_invalid_payload(client):
    response = client.post("/api/add", json={"a": "7", "b": 5})

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Request JSON must include numeric 'a' and 'b' fields."
    }
