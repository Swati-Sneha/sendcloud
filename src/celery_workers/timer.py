from src.celery_workers.celery_app import celery_app
import requests


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
        Webhook for 12345 triggered successfully.
    """
    try:
        print("I am here")
        response = requests.post(url, data={"id": timer_id}, timeout=10.0)
        if response.status_code == 200:
            print(f"Webhook for {timer_id} triggered successfully.")
        else:
            print(f"Webhook for {timer_id} failed with status {response.status_code}")
    except requests.RequestException as e:
        print(f"Error triggering webhook for {timer_id}: {e}")