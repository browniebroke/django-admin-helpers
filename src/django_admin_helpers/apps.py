from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdminHelpersAppConfig(AppConfig):
    """App config for Django Admin Helpers."""

    name = "django_admin_helpers"
    verbose_name = _("admin helpers")
