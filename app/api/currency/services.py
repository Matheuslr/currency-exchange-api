from abc import ABC, abstractmethod
from typing import Dict, List

from app.api.currency.model import CurrenciesPriceOutputSchema, CurrencySchema
from app.api.currency.repository.currency_api import CurrencyExternalAPIRepository
from app.api.currency.repository.database import CurrencyRepository
from app.api.helpers.exception import (
    CurrencyAlreadyExistException,
    CurrencyDoesNotExistException,
    NoCurrencyFoundException,
)
from app.db.mongodb import AsyncIOMotorClient
from app.settings import Settings


class CurrencyServiceAbstract(ABC):
    @abstractmethod
    def get_all_currencies(self):
        raise NotImplementedError

    @abstractmethod
    def create_currency(self, new_currency_schema: CurrencySchema):
        raise NotImplementedError

    @abstractmethod
    def get_currencies_price(self, CurrenciesPriceInputSchema) -> List[Dict]:
        raise NotImplementedError


class CurrencyService(CurrencyServiceAbstract):
    def __init__(self, conn: AsyncIOMotorClient, settings: Settings):
        self.currency_repository = CurrencyRepository(settings, conn)
        self.currency_external_api_repository = CurrencyExternalAPIRepository(settings)

    async def get_all_currencies(self) -> List[CurrencySchema]:
        return await self.currency_repository.get_all_currencies()

    async def create_currency(
        self, new_currency_schema: CurrencySchema
    ) -> CurrencySchema:  # noqa
        await self.__check_if_iso_4217_exists(new_currency_schema.iso_4217)
        currency: CurrencySchema = await self.currency_repository.get_currency(
            new_currency_schema.iso_4217
        )

        is_currency_already_created = currency is not None

        if is_currency_already_created:
            raise CurrencyAlreadyExistException

        return await self.currency_repository.create_currency(
            new_currency_schema
        )  # no qa

    async def get_currencies_price(
        self, CurrenciesPriceInputSchema
    ) -> List[CurrenciesPriceOutputSchema]:
        await self.__check_if_iso_4217_exists(CurrenciesPriceInputSchema.base_currency)

        currencies: List[
            CurrencySchema
        ] = await self.currency_repository.get_all_currencies()

        if len(currencies) == 0:
            raise NoCurrencyFoundException

        currencies_iso4217 = [item.iso_4217 for item in currencies]
        currencies_price = (
            await self.currency_external_api_repository.get_currencies_price(
                currencies_iso4217,
                CurrenciesPriceInputSchema.amount,
                CurrenciesPriceInputSchema.base_currency,
            )
        )
        response_list = []

        for currency in currencies:
            response_list.append(
                CurrenciesPriceOutputSchema(
                    name=currency.name,
                    iso_4217=currency.iso_4217,
                    amount=currencies_price[currency.iso_4217],
                )
            )

        return response_list

    async def __check_if_iso_4217_exists(self, iso_4217):
        is_currency_exists = (
            await self.currency_external_api_repository.check_if_currency_exist(
                iso_4217
            )
        )
        if not is_currency_exists:
            raise CurrencyDoesNotExistException
