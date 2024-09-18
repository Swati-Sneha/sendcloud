from __future__ import annotations

from typing import Optional

from celery import Celery
from kombu import Queue

from src.utilities.singleton import Singleton
from src.utilities.logging_config import setup_logging
from src.settings import settings

setup_logging() 

class CeleryApp(Singleton, Celery):
    """
    A Celery app subclass that ensures only one instance of the Celery app is created
    per process using the Singleton pattern. This avoids issues with creating multiple
    Celery apps within the same process.
    """

    def __init__(self, name: Optional[str] = None) -> None:
        """
        Initializes the Celery app with a given name and the broker URL from settings.

        :param name: Optional name for the Celery app instance.
        """
        
        print(hasattr(self, '_initialized'))
        if not hasattr(self, '_initialized'):
            # Initialize Celery with the provided name and broker URL
            print(settings.CELERY_APP_NAME, name, settings.CELERY_BROKER_URL)
            super().__init__(main=name or settings.CELERY_APP_NAME, broker=settings.CELERY_BROKER_URL)
            self._initialized = True  # Ensure Singleton behavior by tracking initialization

    @classmethod
    def create_app(cls, name: Optional[str] = None) -> CeleryApp:
        """
        Factory method to create or retrieve a singleton instance of the Celery app.

        :param name: Optional name for the Celery app instance.
        :return: Singleton instance of CeleryApp.
        """
        return cls(name)


celery_app = CeleryApp.create_app()

celery_app.conf.task_queues = (
    Queue('webhook_queue', routing_key='webhook.#'),
)

celery_app.conf.task_routes = {
    'src.celery_workers.timer.fire_webhook': {'queue': 'webhook_queue'},
}
celery_app.autodiscover_tasks(['src.celery_workers.timer'])
