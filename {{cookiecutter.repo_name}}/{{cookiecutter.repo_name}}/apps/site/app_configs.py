from django.apps import AppConfig


class DefaultConfig(AppConfig):

    name = 'apps.site'
    verbose_name = 'Site configuration'

    def ready(self):
        # from . import signals
        from . import listeners  # NOQA
