from django.apps import AppConfig


class P2KitchenConfig(AppConfig):
    name = "p2kitchen"
    verbose_name = "Power to kitchen"

    def ready(self):
        import p2kitchen.signals  # noqa
