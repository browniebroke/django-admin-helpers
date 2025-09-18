from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import SafeString, mark_safe

from .conf import app_settings

if TYPE_CHECKING:
    from typing import TypeAlias

    from django.utils.functional import Promise

    StrOrPromise: TypeAlias = str | Promise


def get_app_model_names(model: Model | type[Model]) -> tuple[str, str]:
    """Get app label and model name from private meta attribute."""
    return model._meta.app_label, model._meta.model_name


def admin_list_url(model: type[Model] | Model) -> str:
    """Get the URL to the admin change list for a model."""
    app_label, model_name = get_app_model_names(model)
    return reverse(
        f"{app_settings.ADMIN_HELPERS_URL_NAMESPACE}:"
        f"{app_label}_{model_name}_changelist"
    )


def admin_add_url(model: type[Model]) -> str:
    """Get the URL to the admin add for a model."""
    app_label, model_name = get_app_model_names(model)
    return reverse(
        f"{app_settings.ADMIN_HELPERS_URL_NAMESPACE}:{app_label}_{model_name}_add"
    )


def admin_url(instance: Model) -> str:
    """Get the URL to a model instance in the admin."""
    app_label, model_name = get_app_model_names(instance)
    return reverse(
        f"{app_settings.ADMIN_HELPERS_URL_NAMESPACE}:{app_label}_{model_name}_change",
        kwargs={"object_id": instance.pk},
    )


def admin_link_tag(
    instance: Model | None,
    label: StrOrPromise | None = None,
) -> SafeString:
    """Make a link to a model instance in the admin."""
    if not instance:
        return mark_safe("")
    label = label or str(instance)
    return link_tag(url=admin_url(instance), label=label)


def link_tag(
    url: str,
    label: StrOrPromise | None = None,
    blank: bool = False,
) -> SafeString:
    """Build an HTML tag for a hyperlink."""
    label = label or url
    tag_str = (
        '<a href="{url}" target="_blank">{label}</a>'
        if blank
        else '<a href="{url}">{label}</a>'
    )
    return format_html(tag_str, url=url, label=label)


INLINE_BUTTON_HTML = """
<a href="{url}" class="button"
   style="margin-top: {mt}; margin-bottom: {mb}; display: inline-block;">
    {label}
</a>
"""


def inline_button(
    url: str,
    label: StrOrPromise,
    mt: str = "0",
    mb: str = "1rem",
) -> str:
    """Build a button to be inlined in the admin."""
    return format_html(INLINE_BUTTON_HTML, url=url, label=label, mt=mt, mb=mb)
