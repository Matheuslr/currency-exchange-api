from typing import Dict
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from mongomock import MongoClient

import app.db.mongodb
from app.api.currency.repository import CurrencyRepository
from app.settings import Settings


@pytest.mark.asyncio
async def test_should_get_currency(currencies_payload: Dict):
    mock_currency_repository = AsyncMock()
    mock_currency_repository.get_all_currencies = AsyncMock(
        return_value=currencies_payload
    )

    repositories = await mock_currency_repository.get_all_currencies()

    assert repositories == currencies_payload
    assert mock_currency_repository.get_all_currencies.call_count == 1
