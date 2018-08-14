from django.apps import AppConfig


class EuropartsConfig(AppConfig):
    name = 'europarts'

    def ready(self):
        import europarts.signals