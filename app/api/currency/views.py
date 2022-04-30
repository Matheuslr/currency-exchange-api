from typing import List
from app.api.currency.services import CurrencyService
from fastapi import APIRouter, Depends
from app.db.mongodb import AsyncIOMotorClient, get_database
from app.api.currency.model import CurrencySchema
from app.settings import settings

router = APIRouter()

@router.get("/", response_model=list[CurrencySchema])
async def index(
    conn : AsyncIOMotorClient = Depends(get_database)
):
    """
    List all currencies.

    :param db_session: AsyncSession

    :return: list of currency
    """
    try:
        currency_service: CurrencyService = CurrencyService(conn, settings)
        return await currency_service.get_all_currencies()
    except Exception as e:
        raise e
