from typing import List
from bson.objectid import ObjectId
from pydantic import BaseConfig, BaseModel, Field
from pydantic.class_validators import validator
from datetime import datetime, timezone

from app.api.currency.validators import iso_4217_check


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class CurrencySchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    iso_4217: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

        schema_extra = {"example": {"name": "real", "iso_4217": "BRL"}}

    _iso_4217_check = validator("iso_4217", allow_reuse=True)(iso_4217_check)


# class CurrencyBase(BaseModel):
#     name: str = None
#     iso_4217: str = None

#     class Config:
#         orm_mode = True
#         allow_population_by_alias = True
#         json_encoders = {
#             datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
#             .isoformat()
#             .replace("+00:00", "Z")
#         }


# class CurrenciesResponseSchema(BaseModel):
#     currencies: List[CurrencyBase] = None
#     class Config:
#         orm_mode = True
#         allow_population_by_alias = True
#         json_encoders = {
#             datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
#             .isoformat()
#             .replace("+00:00", "Z")
#         }

