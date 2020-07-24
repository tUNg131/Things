from django.apps import AppConfig


class CollectConfig(AppConfig):
    name = 'collect'

    def ready(self):
        from . import signals
