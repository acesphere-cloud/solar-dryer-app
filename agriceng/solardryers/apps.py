
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SolarDryerConfig(AppConfig):
    name = "agriceng.solardryers"
    verbose_name = _("Solar Dryers")

    def ready(self):
        try:
            import agriceng.solardryers.signals  # noqa F401
        except ImportError:
            pass
