from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from pydantic.class_validators import validator

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

    # @classmethod
    # def __modify_schema__(cls, field_schema):
    #     field_schema.update(type="string")


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
