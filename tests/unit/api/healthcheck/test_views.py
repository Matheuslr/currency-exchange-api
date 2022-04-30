from time import time

from freezegun import freeze_time

from tests.conftest import TestClient


def test_should_get_app(client: TestClient):
    response = client.get("/")
    result = response.json()

    assert response.status_code == 200
    assert result == [{"app": "sbf-challenge"}]


@freeze_time("2022-01-14")
def test_should_get_health(client: TestClient):
    response = client.get("/health")
    result = response.json()

    assert response.status_code == 200
    assert result == {"healthy": True, "checked_at": time()}
