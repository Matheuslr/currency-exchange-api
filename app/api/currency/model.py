"""app models."""


from pydantic import BaseModel
from pydantic.class_validators import validator

from app.api.currency.validators import iso_4217_check


class CurrencySchema(BaseModel):
    name: str
    iso_4217: str

    _iso_4217_check = validator("iso_4217", allow_reuse=True)(iso_4217_check)
