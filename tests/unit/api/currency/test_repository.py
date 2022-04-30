import pytest
import app.db.mongodb
from typing import Dict
from unittest.mock import AsyncMock, MagicMock, Mock, patch

from app.api.currency.repository import CurrencyRepository
from app.settings import Settings
from mongomock import MongoClient

@pytest.mark.asyncio
async def test_should_get_currency(currencies_payload:Dict):
    mock_currency_repository = AsyncMock()
    mock_currency_repository.get_all_currencies = AsyncMock(return_value = currencies_payload)

    repositories = await mock_currency_repository.get_all_currencies()

    assert repositories == currencies_payload
    assert mock_currency_repository.get_all_currencies.call_count == 1

