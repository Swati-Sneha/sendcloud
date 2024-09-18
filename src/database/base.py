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
    Generic Class for handling the low level database operation: Create,
    Read, Update, Delete object.

    How to create a subclass:
        Your model must inherit from BaseDBModel:
        >>> class Thing(BaseDBModel): ...

        BaseCrud is Generic -- it encapsulates some abstract ModelType,
        and it knows that ModelType must be a subclass of BaseDBModel
        (because of the `bound=BaseDBModel`), but beyond that, BaseCrud
        doesn't have a concrete value for ModelType.

        Subclasses need to specify the concrete value for ModelType, which in
        this case is `Thing`:
        >>> class ThingsDB(BaseCrud[Thing]): ...
        >>> things_db = ThingsDB()

        Specifying the concrete type allows mypy and IDEs to see that
        `ModelType` actually means `Thing`, when dealing with `ThingsDB`.
        For example, say BaseCrud defines a method which returns a `ModelType`:
        >>> class BaseCrud:
        ...     def foo(self) -> ModelType: ...

        Mypy and IDEs will know that the return value of this statement
        >>> things_db.foo()
        is `Thing`, not `ModelType`. This makes for better code analysis and
        tab completion.
    """

    _model_class: type[ModelType]
    _collection_name: str

    def __init__(self) -> None:
        """Init the BaseCrud instance and set the collection document link to the model."""
        if not (self._model_class and self._collection_name):
            raise RuntimeError("Model or collection name is missing initialising DB interface.")

    @property
    def _collection(self) -> AsyncIOMotorCollection:
        return Database().db[self._collection_name]

    async def get(self, query: dict[str, Any], *args: Any, **kwargs: Any) -> Union[ModelType, None]:
        """Get one object from the DB."""
        obj = await self._collection.find_one(query, *args, **kwargs)

        if obj:
            return self._model_class(**obj)

        return None

    async def find(
        self, query_param: dict[str, Any], sort_param:  Optional[List[Tuple[str, Any]]]
    ) -> list[ModelType]:
        """Find objects in the DB based on the query."""
        cursor = self._collection.find(query_param)

        if sort_param:
            cursor = cursor.sort(sort_param)

        return [self._model_class(**doc) async for doc in cursor]

    async def create(self, obj: ModelType) -> ObjectId:
        """
        Insert given object in the database.
        @param obj: model object to be inserted in the DB.
        @return: ObjectId on an inserted document
        """
        if not isinstance(obj, self._model_class):
            raise RuntimeError(f"Can't insert object of type {type(obj)} into {self._collection_name} collection.")

        obj_dict = obj.dict()
        result = await self._collection.insert_one(obj_dict)

        return result.inserted_id

    async def update(
        self,
        lookup: dict[str, Any],
        update: dict[str, Any],
        action: str = "$set",
        return_document: bool = ReturnDocument.AFTER,
    ) -> Union[ModelType, None]:
        """
        Update document in the db and.
        @param lookup: lookup for an object to be updated
        @param update: the updates to be applied
        @param action: indicates what update should happen i.e. $set, $push, $pull, etc.
        @param return_document: indicator to return document before of after update
        @return: object
        """
        if action == "$set":
            update["updated"] = datetime.utcnow()
            db_update = {action: update}
        else:
            db_update = {"$set": {"updated": datetime.utcnow()}, action: update}

        result = await self._collection.find_one_and_update(lookup, db_update, return_document=return_document)

        if not result:
            return None

        return self._model_class(**result)

    async def create_or_update_one(self, lookup: dict[str, Any], update: dict[str, Any], upsert: bool) -> UpdateResult:
        """
        Create or update one document.

        :param lookup: the filter
        :param update: the update
        :param upsert: whether to do an upsert
        :return: update result
        """
        return await self._collection.update_one(lookup, update, upsert=upsert)

    async def delete(self, query: dict[str, Any]) -> DeleteResult:
        """Delete object."""
        return await self._collection.delete_one(query)
