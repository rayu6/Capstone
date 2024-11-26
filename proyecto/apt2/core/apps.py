from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

class AptConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apt'

    def ready(self):
        import core.signals  # importa las señales
