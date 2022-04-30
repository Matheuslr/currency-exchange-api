from abc import ABC, abstractmethod
from typing import List

from app.api.currency.model import CurrencySchema
from app.db.mongodb import AsyncIOMotorClient
from app.settings import Settings


class CurrencyRepositoryAbstract(ABC):
    @abstractmethod
    def get_all_currencies(self):
        raise NotImplementedError


class CurrencyRepository(CurrencyRepositoryAbstract):
    def __init__(self, settings: Settings, conn: AsyncIOMotorClient) -> None:
        self.conn = conn
        self._settings = settings

    async def get_all_currencies(self):
        currencies: List[CurrencySchema] = []

        rows = self.conn[self._settings.mongo_database_name][
            self._settings.currency_collection_name
        ].find()

        async for row in rows:
            currencies.append(CurrencySchema(**row))

        return currencies
