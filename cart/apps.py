from django.apps import AppConfig


class CartConfig(AppConfig):

    name = 'cart'
    verbose_name = 'Cart'

    def ready(self):

        # import signal handlers
        import cart.signals.handlers