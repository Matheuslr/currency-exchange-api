from unittest.mock import MagicMock, patch

import httpx
import pytest
from deepdiff import DeepDiff
from fastapi.testclient import TestClient
from mongomock import MongoClient
from requests import Response
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_503_SERVICE_UNAVAILABLE,
)

from app.api.helpers.exception import CurrencyDoesNotExistException
from app.settings import settings


@pytest.mark.asyncio
async def test_get_all_currencies_view(client: TestClient, mongo_db: MongoClient):
    response = client.get("/api/currency/")

    result = response.json()
    result_ids = set([item["_id"] for item in result])

    database_currencies_cursor = mongo_db[settings.mongo_test_database_name][
        settings.currency_collection_name
    ].find()
    database_ids = set([item["_id"].__str__() for item in database_currencies_cursor])
    assert result_ids == database_ids
    assert response.status_code == HTTP_200_OK


def test_shoud_create_a_currency(client: TestClient, currency_payload: dict):
    response = client.post("/api/currency/", json=currency_payload)
    result = response.json()
    del result["_id"]

    assert result == currency_payload
    assert response.status_code == HTTP_201_CREATED


@pytest.mark.parametrize(
    "wrong_iso",
    ["BR", "BRLL", "123", ""],
)
def test_shoud_not_create_a_currency_with_wrong_iso_4217(
    client: TestClient, currency_payload: dict, wrong_iso
):
    wrong_currency_payload = currency_payload.copy()
    wrong_currency_payload["iso_4217"] = wrong_iso
    response = client.post("/api/currency/", json=wrong_currency_payload)

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_shoud_not_create_a_currency_with_inexistent_iso_4217(
    client: TestClient,
    currency_payload: dict,
):
    with patch(
        "app.api.currency.repository.currency_api.CurrencyExternalAPIRepository.check_if_currency_exist"
    ) as mocky:
        mocky.return_value = False
        wrong_currency_payload = currency_payload.copy()
        wrong_currency_payload["iso_4217"] = "XMR"
        response = client.post("/api/currency/", json=wrong_currency_payload)
        assert response.status_code == HTTP_404_NOT_FOUND


def test_shoud_not_create_an_already_created_currency(
    client: TestClient, currency_payload: dict
):
    with patch(
        "app.api.currency.repository.currency_api.CurrencyExternalAPIRepository.check_if_currency_exist"
    ) as mocky:
        mocky.return_value = True
        wrong_currency_payload = currency_payload.copy()
        wrong_currency_payload["iso_4217"] = "BRL"
        response = client.post("/api/currency/", json=wrong_currency_payload)

    assert response.status_code == HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_shoud_not_create_currency_when_external_service_is_down(
    client: TestClient, currency_payload: dict
):
    with patch(
        "app.api.currency.repository.currency_api.httpx.AsyncClient.get"
    ) as mocky:
        mocky.side_effect = httpx.RequestError("error")
        response = client.post("/api/currency/", json=currency_payload)

    assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE


@patch(
    "app.api.currency.repository.currency_api.CurrencyExternalAPIRepository.check_if_currency_exist"
)
def test_shoud_get_currencies_price(
    mock_check_if_currency_exist: MagicMock,
    client: TestClient,
    mongo_db: MongoClient,
    currencies_payload: dict,
    exchangerate_api_response: dict,
    currencies_price_payload: dict,
):

    expected_payload = [
        {"name": "real", "iso_4217": "BRL", "amount": 1.0},
        {"name": "dolar", "iso_4217": "USD", "amount": 0.2},
    ]
    mock_check_if_currency_exist.return_value = True
    mongo_db[settings.mongo_test_database_name][
        settings.currency_collection_name
    ].insert_many(currencies_payload)
    with patch(
        "app.api.currency.repository.currency_api.CurrencyExternalAPIRepository.get_currencies_price"
    ) as mocky:
        mocky.return_value = exchangerate_api_response["rates"]
        response = client.post(
            "/api/currency/currencies-price", json=currencies_price_payload
        )
        result = response.json()
        assert DeepDiff(expected_payload, result)
        assert response.status_code == HTTP_200_OK


@pytest.mark.parametrize(
    "wrong_iso",
    ["BR", "BRLL", "123", ""],
)
def test_shoud_not_get_currencies_price_with_wrong_iso_4217(
    client: TestClient, currencies_price_payload: dict, wrong_iso
):
    wrong_currency_payload = currencies_price_payload.copy()
    wrong_currency_payload["base_currency"] = wrong_iso
    response = client.post(
        "/api/currency/currencies-price", json=wrong_currency_payload
    )

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_shoud_not_get_currencies_price_with_empty_database(
    client: TestClient,
    currencies_price_payload: dict,
):
    with patch(
        "app.api.currency.repository.database.CurrencyRepository.get_all_currencies"
    ) as mocky:
        mocky.return_value = []
        wrong_currency_payload = currencies_price_payload.copy()
        wrong_currency_payload["iso_4217"] = "BRL"
        response = client.post(
            "/api/currency/currencies-price", json=wrong_currency_payload
        )
        assert response.status_code == HTTP_404_NOT_FOUND


def test_shoud_not_get_currencies_price_with_inexistent_iso_4217(
    client: TestClient,
    currencies_price_payload: dict,
):
    with patch(
        "app.api.currency.repository.currency_api.CurrencyExternalAPIRepository.check_if_currency_exist"
    ) as mocky:
        mocky.return_value = False
        wrong_currency_payload = currencies_price_payload.copy()
        wrong_currency_payload["iso_4217"] = "XMR"
        response = client.post(
            "/api/currency/currencies-price", json=wrong_currency_payload
        )
        assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_shoud_not_get_currencies_price_when_external_service_is_down(
    client: TestClient, currencies_price_payload: dict
):
    with patch(
        "app.api.currency.repository.currency_api.httpx.AsyncClient.get"
    ) as mocky:
        mocky.side_effect = httpx.RequestError("error")
        response = client.post(
            "/api/currency/currencies-price", json=currencies_price_payload
        )

    assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE
