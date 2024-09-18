from unittest.mock import patch
import pytest

@pytest.fixture
def setup_mocks():
    """Fixture to setup mocks for `requests.post` and `timer.update_timer_request`."""
    with patch('src.celery_workers.timer.requests.post') as mock_post, \
         patch('src.database.timer.timer.update_timer_request') as mock_update_timer:
        yield mock_post, mock_update_timer