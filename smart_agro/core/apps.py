from django.apps import AppConfig


class SmartagroConfig(AppConfig):
    name = 'smart_agro.core'

    def ready(self):
        from . import signals