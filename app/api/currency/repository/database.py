from abc import ABC, abstractmethod
from typing import List

from bson.objectid import ObjectId

from app.api.currency.model import CurrencySchema
from app.db.mongodb import AsyncIOMotorClient
from app.settings import Settings


class CurrencyRepositoryAbstract(ABC):
    @abstractmethod
    async def get_currency(self, iso_4217: str) -> CurrencySchema:
        raise NotImplementedError

    @abstractmethod
    async def get_all_currencies(self) -> List[CurrencySchema]:
        raise NotImplementedError

    @abstractmethod
    async def create_currency(self, name: str, iso_4217: str) -> CurrencySchema:
        raise NotImplementedError

    @abstractmethod
    async def update_currency(self, _id:ObjectId, name: str =None, iso_4217: str=None) -> CurrencySchema:
        raise NotImplementedError

    # @abstractmethod
    # async def delete_currency(self, _id:ObjectId) -> CurrencySchema:
    #     raise NotImplementedError


class CurrencyRepository(CurrencyRepositoryAbstract):
    def __init__(self, settings: Settings, conn: AsyncIOMotorClient):
        self.conn = conn
        self._settings = settings
        self._database_name = (
            settings.mongo_test_database_name
            if settings.test
            else settings.mongo_database_name
        )

    async def get_currency(self, iso_4217: str) -> List[CurrencySchema]:
        return await self.conn[self._database_name][
            self._settings.currency_collection_name
        ].find_one({"iso_4217": iso_4217})

    async def get_all_currencies(self) -> List[CurrencySchema]:
        currencies: List[CurrencySchema] = []

        rows = self.conn[self._database_name][
            self._settings.currency_collection_name
        ].find()

        async for row in rows:
            currencies.append(CurrencySchema(**row))

        return currencies

    async def create_currency(
        self, new_currency_schema: CurrencySchema
    ) -> CurrencySchema:
        currency_dict = dict(
            name=new_currency_schema.name, iso_4217=new_currency_schema.iso_4217
        )
        await self.conn[self._database_name][
            self._settings.currency_collection_name
        ].insert_one(currency_dict)

        return CurrencySchema(**currency_dict)


    async def update_currency(self, _id:str, update_dict) -> CurrencySchema:

        await self.conn[self._database_name][
            self._settings.currency_collection_name
        ].update_one({"_id": _id},{"$set": update_dict})

