from datetime import datetime, timezone
from typing import Any, Generic, Mapping, Tuple, TypeVar, Union, Optional, List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import DESCENDING, ReturnDocument
from pymongo.results import DeleteResult, UpdateResult

from src.database.db import Database
from src.models.base import BaseDBModel


ModelType = TypeVar("ModelType", bound=BaseDBModel)
DocumentType = TypeVar("DocumentType", bound=Mapping[str, Any])


class BaseCrud(Generic[ModelType]):
    """
    A base class for CRUD (Create, Read, Update, Delete) operations that provides
    an interface to interact with a MongoDB collection. The class is designed to 
    be extended by specific models to allow for reusable and consistent database operations.

    Attributes:
        _model_class (type[ModelType]): The model class that defines the structure 
                                        and validation for the data in the MongoDB collection.
        _collection_name (str): The name of the MongoDB collection associated with the model.
    
    Properties:
        _collection (AsyncIOMotorCollection): Provides an async interface to the MongoDB collection 
                                              corresponding to the `_collection_name`.
    """

    _model_class: type[ModelType]
    _collection_name: str

    def __init__(self) -> None:
        """
        Initializes the BaseCrud instance by ensuring that both the model class (`_model_class`) 
        and the collection name (`_collection_name`) are provided.

        Raises:
            RuntimeError: If either the model class or the collection name is missing when 
                          initializing the database interface.
        """
        if not (self._model_class and self._collection_name):
            raise RuntimeError("Model or collection name is missing initialising DB interface.")

    @property
    def _collection(self) -> AsyncIOMotorCollection:
        return Database().db[self._collection_name]

