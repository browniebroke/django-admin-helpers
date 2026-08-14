from __future__ import annotations

import logging
from typing import ClassVar

from django.db.models import Model, QuerySet
from django.http import HttpRequest

logger = logging.getLogger(__name__)


class FilesDeleteMixin:
    """
    Mixin for ``ModelAdmin`` classes to delete files along with model instances.

    By default, Django leaves the files of ``FileField`` (and ``ImageField``)
    in storage when the model instances referencing them are deleted. This
    mixin hooks into the admin deletion flow to also delete the files from
    storage, both when deleting a single instance from its change page and
    when using the bulk delete action from the change list.

    Set the ``file_field_names`` attribute to the list of file field names
    to delete (defaults to ``["file"]``)::

        class DocumentAdmin(FilesDeleteMixin, admin.ModelAdmin):
            file_field_names = ["file", "thumbnail"]

    If a file cannot be deleted, the error is logged and the instance is
    deleted from the database anyway.
    """

    file_field_names: ClassVar[list[str]] = ["file"]

    def delete_model(self, request: HttpRequest, obj: Model) -> None:
        """Delete the file(s) associated with the instance."""
        self._delete_files_from_obj(obj)
        super().delete_model(request, obj)  # type: ignore[misc]

    def delete_queryset(self, request: HttpRequest, queryset: QuerySet[Model]) -> None:
        """Delete the file(s) associated with the instances in the queryset."""
        for obj in queryset:
            self._delete_files_from_obj(obj)
        super().delete_queryset(request, queryset)  # type: ignore[misc]

    def _delete_files_from_obj(self, obj: Model) -> None:
        """Delete the file(s) associated with the model instance."""
        for field_name in self.file_field_names:
            try:
                getattr(obj, field_name).delete(save=False)
            except Exception as exc:
                logger.exception(
                    "Could not delete file on field '%s' from %s (%r) "
                    "- proceeding with deleting record from DB",
                    field_name,
                    obj,
                    exc,
                )
