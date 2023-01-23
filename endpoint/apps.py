from django.apps import AppConfig


class EndpointConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'endpoint'

    def ready(self) -> None:
        from endpoint.cron import main_loop_thread
        from threading import Thread
        from config.settings import REQUEST_INTERVAL

        Thread(target=main_loop_thread, args=[REQUEST_INTERVAL], daemon=True).start()
        return super().ready()
