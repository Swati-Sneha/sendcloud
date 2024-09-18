from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from http import HTTPStatus
from datetime import datetime, timedelta, timezone
from pydantic import ValidationError
from bson import ObjectId
from bson.errors import InvalidId

import math
from src.models.timer import SetTimerRequest, SetTimerResponse, GetTimerResponse
from src.celery_workers import timer as timer_celery
from src.database.timer import timer

timerRoutes = APIRouter()

@timerRoutes.post('/')
async def set_timer(request: Request):
    """
    Route to accept timer request.
    Saves the request in db and triggers celery task to trigger url at calculated eta.
    """
    if not request.headers.get('Content-Type') == 'application/json':
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Request must be in JSON format")

    data = await request.json()

    try:
        timer_data = SetTimerRequest(**data)

        hours = timer_data.hours
        minutes = timer_data.minutes
        seconds = timer_data.seconds
        url = str(timer_data.url)
        
        eta = datetime.now(tz=timezone.utc) + timedelta(hours=hours, minutes=minutes, seconds=seconds)

        timer_db = await timer.insert_timer_request(eta=eta, url=url)

        timer_celery.fire_webhook.apply_async((str(timer_db.id), url), eta=eta, queue="webhook_queue")

        response = SetTimerResponse(
            id=str(timer_db.id),
            time_left=hours * 3600 + minutes * 60 + seconds
        )

    except ValidationError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=e.errors()) from e
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.") from e

    return JSONResponse(content=response.model_dump(), status_code=HTTPStatus.CREATED)


@timerRoutes.get('/{timer_id}')
async def get_timer(timer_id: str):
    try:
        timer_id = ObjectId(timer_id)
    except InvalidId as exc:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Invalid timer ID format."
        ) from exc

    timer_db = await timer.get_timer_by_id(timer_id=timer_id)

    if not timer_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Timer not found")

    time_now = datetime.now(tz=timezone.utc).replace(tzinfo=None)
    response = GetTimerResponse(id=timer_db.id, time_left=0)

    if time_now > timer_db.eta:
        return JSONResponse(content=response.model_dump(), status_code=HTTPStatus.OK)

    response.time_left = math.floor((timer_db.eta - time_now).total_seconds())

    return JSONResponse(content=response.model_dump(), status_code=HTTPStatus.OK)
