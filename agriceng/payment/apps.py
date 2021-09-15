from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PaymentConfig(AppConfig):
    name = "agriceng.payment"
    verbose_name = _("Payment")

    def ready(self):
        try:
            import agriceng.payment.signals  # noqa F401
        except ImportError:
            pass
