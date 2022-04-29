from unittest.mock import MagicMock, patch

import pytest

from app.api.currency.model import CurrencySchema


def test_should_create_currency(currency_payload: dict):
    currency_schema: CurrencySchema = CurrencySchema(**currency_payload)

    assert currency_schema.name == currency_payload["name"]
    assert currency_schema.iso_4217 == currency_payload["iso_4217"]


@pytest.mark.parametrize(
    "wrong_iso",
    ["BR", "BRLL", "123", ""],
)
@patch("app.api.currency.model.CurrencySchema")
def test_should_create_currency_with_invalid_iso_4217(
    mock_currency_model: MagicMock, wrong_iso: str, currency_payload: dict
):
    wrong_data = currency_payload.copy()
    wrong_data["iso_4217"] = wrong_iso
    with pytest.raises(ValueError):
        CurrencySchema(**wrong_data)
        assert mock_currency_model.assert_called_once()
