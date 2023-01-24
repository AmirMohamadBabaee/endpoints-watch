import sys
from django.apps import AppConfig


class EndpointConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'endpoint'
    background_thread = None

    def ready(self) -> None:
        from endpoint.cron import main_loop_thread
        from threading import Thread
        from config.settings import REQUEST_INTERVAL

        if sys.argv[1] == 'runserver':
            self.background_thread = Thread(target=main_loop_thread, args=[REQUEST_INTERVAL], daemon=True)
            self.background_thread.start()
        return super().ready()
