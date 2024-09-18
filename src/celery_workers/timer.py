import requests
import logging
import asyncio
from src.celery_workers.celery_app import celery_app
from src.database.timer import timer

logger = logging.getLogger(__name__)

@celery_app.task
def fire_webhook(timer_id, url) -> None:
    """
    Triggers a webhook by sending a POST request to the specified URL with the timer ID as data.

    This task is designed to be executed asynchronously by Celery. It sends a POST request
    to the provided URL with a payload containing the `timer_id`. The function logs the outcome
    of the request, including successful triggers and any errors encountered.

    Args:
        timer_id (str): The unique identifier of the timer to be included in the request payload.
        url (str): The URL to which the POST request should be sent.

    Returns:
        None

    Raises:
        requests.RequestException: If an error occurs while sending the POST request, such as a network error
        or an invalid response.

    Example:
        >>> fire_webhook("12345", "https://example.com/webhook")
    """
    try:
        logger.info("Triggering request to %s, for timer_id %s", url, timer_id)
        update_dict = {}
        response = requests.post(url, data={"id": timer_id}, timeout=10.0)
        if response.status_code == 200:
            logger.info("Webhook for %s triggered successfully.", timer_id)
            update_dict = {"$set": {"status_code": 200, "success": True, "response": response.text}}
        else:
            logger.info("Webhook for %s failed with status %s", timer_id, response.status_code)
            update_dict = {"$set": {"status_code": response.status_code, "success": False, "response": response.text}}
    except requests.RequestException as e:
        logger.warning("Error triggering webhook for %s: %s", timer_id, e)
        update_dict = {"$set": {"success": False, "response": str(e)}}
    finally:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(timer.update_timer_request(timer_id=timer_id, update_obj=update_dict))

