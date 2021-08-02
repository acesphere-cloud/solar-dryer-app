
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AreaConfig(AppConfig):
    name = "agriceng.area"
    verbose_name = _("Area")

    def ready(self):
        try:
            import agriceng.area.signals  # noqa F401
        except ImportError:
            pass
