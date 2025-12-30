from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RenovationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'renovation'
    verbose_name = _('Remont')
