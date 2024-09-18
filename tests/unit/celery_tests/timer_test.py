import requests
from unittest.mock import MagicMock

from src.celery_workers.timer import fire_webhook


def test_fire_webhook_success(setup_mocks):
    """Test with `fire_webhook` successful request."""
    mock_post, mock_update_timer = setup_mocks

    mock_post.return_value = MagicMock(status_code=200, text="Success")

    fire_webhook('test_timer_id', 'http://example.com/webhook')

    mock_post.assert_called_once_with('http://example.com/webhook', data={"id": 'test_timer_id'}, timeout=10.0)

    expected_update_dict = {"$set": {"status_code": 200, "success": True, "response": "Success"}}
    mock_update_timer.assert_called_once_with(timer_id='test_timer_id', update_obj=expected_update_dict)


def test_fire_webhook_failure(setup_mocks):
    """Test with `fire_webhook` on a failed request."""
    mock_post, mock_update_timer = setup_mocks

    mock_post.return_value = MagicMock(status_code=500, text="Error")

    fire_webhook('test_timer_id', 'http://example.com/webhook')

    mock_post.assert_called_once_with('http://example.com/webhook', data={"id": 'test_timer_id'}, timeout=10.0)
    
    expected_update_dict = {"$set": {"status_code": 500, "success": False, "response": "Error"}}
    mock_update_timer.assert_called_once_with(timer_id='test_timer_id', update_obj=expected_update_dict)


def test_fire_webhook_exception(setup_mocks):
    """Test that `fire_webhook` handles exceptions gracefully."""
    mock_post, mock_update_timer = setup_mocks

    mock_post.side_effect = requests.RequestException("Network error")

    fire_webhook('test_timer_id', 'http://example.com/webhook')

    mock_post.assert_called_once_with('http://example.com/webhook', data={"id": 'test_timer_id'}, timeout=10.0)

    expected_update_dict = {"$set": {"success": False, "response": "Network error"}}
    mock_update_timer.assert_called_once_with(timer_id='test_timer_id', update_obj=expected_update_dict)
