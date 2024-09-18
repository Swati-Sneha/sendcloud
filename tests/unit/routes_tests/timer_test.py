import pytest
import httpx
from app import app
from datetime import datetime, timezone, timedelta
from bson import ObjectId
from unittest.mock import patch, Mock, MagicMock

@pytest.mark.anyio
@patch('src.celery_workers.timer.fire_webhook.apply_async')
async def test_set_timer(mock_apply_async: Mock, async_client: httpx.AsyncClient):
    payload = {
        "hours": 1,
        "minutes": 30,
        "seconds": 15,
        "url": "http://example.com/webhook"
    }
        
    mock_apply_async.return_value = None

    # Successful Response
    response = await async_client.post("/", json=payload, headers={"Content-Type": "application/json"})

    assert response.status_code == 201
    response_data = response.json()
    assert "id" in response_data
    assert "time_left" in response_data
    assert mock_apply_async.called

    # Not a json request
    response = await async_client.post("", data="invalid json")
    assert response.status_code == 400
    assert response.json() == {"detail": "Request must be in JSON format"}
    
    # Invalid request
    response = await async_client.post("", json={"hours": 1}, headers={"Content-Type": "application/json"})
    assert response.status_code == 422


@pytest.mark.anyio
@patch('src.database.timer.Timer.get_timer_by_id') 
async def test_get_timer(mock_get_timer_by_id: MagicMock, async_client: httpx.AsyncClient):
    # Prepare mock data
    timer_id = ObjectId()
    mock_timer = MagicMock()
    mock_timer.id = str(timer_id)
    mock_timer.eta = (datetime.now(tz=timezone.utc) + timedelta(hours=1, minutes=30, seconds=15)).replace(tzinfo=None)
    
    # Mock the behavior of get_timer_by_id
    mock_get_timer_by_id.return_value = mock_timer

    # Make the GET request
    response = await async_client.get(f"/{timer_id}")

    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert "time_left" in response_data

    # Test invalid ID format
    response = await async_client.get("/invalid_id")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid timer ID format."}

    # Test non-existent timer
    mock_get_timer_by_id.return_value = None
    non_existent_id = ObjectId()
    response = await async_client.get(f"/{non_existent_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Timer not found"}
