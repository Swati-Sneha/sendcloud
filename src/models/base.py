
from datetime import datetime, timezone
from typing import Any, Dict, Generic, Optional, TYPE_CHECKING, Tuple, Type, TypeVar, Union

from bson import ObjectId
from pydantic import Field
from pydantic.main import BaseModel

from src.models.custom_models import PyObjectId
from src.constants import DATE_TIME_FORMAT


class BaseDBModel(BaseModel):
    """Base database model to be used for every model meant to be saved in the DB."""

    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    created: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    updated: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))


    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda x: x.strftime(DATE_TIME_FORMAT)}

    def dict(
        self,
        *,
        by_alias: bool = False,
    ) -> dict:
        output_dict = super().model_dump(by_alias=by_alias)
        
        print(output_dict)

        # Override the `_id` field in MongoDB and remove the Pydantic `id` field
        if "id" in output_dict:
            output_dict["_id"] = str(output_dict.pop("id"))

        return output_dict