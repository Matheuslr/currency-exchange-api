from abc import ABC, abstractmethod
from typing import List
from app.api.currency.model import CurrencySchema
from app.settings import Settings
from app.api.currency.repository import CurrencyRepository
from app.db.mongodb import AsyncIOMotorClient

class CurrencyServiceAbstract(ABC):
    @abstractmethod
    def get_all_currencies(self):
        raise NotImplementedError
class CurrencyService(CurrencyServiceAbstract):

    def __init__(self,
    conn:AsyncIOMotorClient,
    settings:Settings):
        self.currency_repository = CurrencyRepository(settings, conn)

    async def get_all_currencies(self) -> List[CurrencySchema]:
        return await self.currency_repository.get_all_currencies()
