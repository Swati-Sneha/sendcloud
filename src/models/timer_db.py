from datetime import datetime
from typing import Optional
from bson import ObjectId

from src.database.base import BaseDBModel


class TimerDB(BaseDBModel):
    """Representation of timer requests stored in the DB."""
    
    eta: datetime
    url: str
    user_id: Optional[ObjectId] = None
    response: Optional[str] = None
    success: Optional[bool] = None
