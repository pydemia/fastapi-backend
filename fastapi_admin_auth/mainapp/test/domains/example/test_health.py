import pytest
import httpx


@pytest.fixture()
def setup():
    # code to tear down test environm
    pass


@pytest.fixture()
def teardown():
    # code to tear down test environment
    pass

@pytest.mark.usefixtures("setup", "teardown")
def test_health_live():

    from fastapi.testclient import TestClient
    from mainapp.main import app
    
    test_client = TestClient(app)

    response = test_client.get("/example/health/live")
    try:
        response.raise_for_status()
        body = response.json()
        assert body["code"] == 1
    except httpx.HTTPStatusError:
        print(response.json()["message"])


@pytest.mark.usefixtures("setup", "teardown")
def test_health_ready():

    from fastapi.testclient import TestClient
    from mainapp.main import app
    
    test_client = TestClient(app)

    response = test_client.get("/example/health/ready")
    try:
        response.raise_for_status()
        body = response.json()
        assert body["code"] == 1
    except httpx.HTTPStatusError:
        print(response.json()["message"])
