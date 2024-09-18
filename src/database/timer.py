from datetime import datetime, timezone
from typing import Any, Optional, Union
from bson import ObjectId

from src.database.base import BaseCrud
from src.models.timer_db import TimerDB


class Timer(BaseCrud[TimerDB]):
    """Handle DB operations upon users collection."""

    _model_class = TimerDB
    _collection_name = "timer"

    def serialize_data(self, obj):
        # Convert the ObjectId to a string
        if '_id' in obj and isinstance(obj['_id'], ObjectId):
            obj['_id'] = str(obj['_id'])
        return obj

    async def insert_timer_request(
        self,
        eta: datetime,
        url: str,
        user_id: Optional[ObjectId] = None,
    ) -> TimerDB:
        """
        Inserts a new timer request into the database.

        :param eta: ETA for timer trigger
        :param url: The URL that should be called when the timer expires
        :param user_id: Optional user ID associated with this timer request
        :return: The inserted TimerDB object
        """
        timer_data = TimerDB(
            eta=eta,
            url=url,
            created=datetime.now(tz=timezone.utc),
            updated=datetime.now(tz=timezone.utc),
            user_id=user_id,
        )

        await self._collection.insert_one(timer_data.dict(by_alias=True))
        return timer_data

    async def update_timer_request(
        self,
        timer_id: ObjectId,
        update_obj: dict[str, Any],
        user_id: Optional[ObjectId] = None,
    ) -> Union[TimerDB, None]:
        """
        Update a delivery job with the given update. This function both ensures the updated field is updated as well,
        and adds a delivery job status change object to the history when needed.

        :param timer_id: the id of the delivery job that needs to be updated (used for filter
        :param updateObj: the update dict
        :param user_id: the id of the user that triggered a change (courier-app) or None (deliverect)
        :return: updated delivery job in case everything went fine, otherwise None
        """
        update_obj["$set"] = {**update_obj.get("$set", {}), **{"updated": datetime.now(tz=timezone.utc)}}
        
        if user_id:
            update_obj["$set"]["user_id"] = user_id

        result = await self._collection.find_one_and_update(
            filter={"_id": timer_id}, update=update_obj, return_document=True
        )
        return TimerDB(**result) if result else None
    
    async def get_timer_by_id(
        self,
        timer_id: ObjectId,
    ) -> Union[TimerDB, None]:
        """
        Update a delivery job with the given update. This function both ensures the updated field is updated as well,
        and adds a delivery job status change object to the history when needed.

        :param timer_id: the id of the delivery job that needs to be updated (used for filter
        :param updateObj: the update dict
        :param user_id: the id of the user that triggered a change (courier-app) or None (deliverect)
        :return: updated delivery job in case everything went fine, otherwise None
        """
        result = await self._collection.find_one({"_id": timer_id})

        if result:
            # Convert the ObjectId to a string
            result['_id'] = str(result['_id'])

        return TimerDB(**result) if result else None


timer = Timer()
