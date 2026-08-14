import logging
from typing import ClassVar

import pytest
from django.contrib import admin
from django.core.files.base import ContentFile

from django_admin_helpers.mixins import FilesDeleteMixin

from .testapp.models import Author, Blog


class AuthorAdmin(FilesDeleteMixin, admin.ModelAdmin):
    file_field_names: ClassVar[list[str]] = ["picture", "attachment"]


class BlogAdmin(FilesDeleteMixin, admin.ModelAdmin):
    pass


@pytest.fixture
def author_admin():
    return AuthorAdmin(Author, admin.AdminSite())


def make_author(suffix="", with_attachment=False):
    author = Author(full_name=f"Author {suffix}")
    author.picture.save(f"picture{suffix}.png", ContentFile(b"fake image"), save=False)
    if with_attachment:
        author.attachment.save(
            f"attachment{suffix}.txt", ContentFile(b"fake file"), save=False
        )
    author.save()
    return author


@pytest.mark.django_db
def test_delete_model_deletes_file(rf, author_admin):
    author = make_author()
    storage = author.picture.storage
    picture_name = author.picture.name
    assert storage.exists(picture_name)

    author_admin.delete_model(rf.post("/"), author)

    assert not storage.exists(picture_name)
    assert not Author.objects.exists()


@pytest.mark.django_db
def test_delete_model_deletes_all_listed_files(rf, author_admin):
    author = make_author(with_attachment=True)
    storage = author.picture.storage
    file_names = [author.picture.name, author.attachment.name]

    author_admin.delete_model(rf.post("/"), author)

    assert not any(storage.exists(name) for name in file_names)
    assert not Author.objects.exists()


@pytest.mark.django_db
def test_delete_queryset_deletes_files(rf, author_admin):
    authors = [make_author(suffix=str(i)) for i in range(3)]
    storage = authors[0].picture.storage
    picture_names = [author.picture.name for author in authors]

    author_admin.delete_queryset(rf.post("/"), Author.objects.all())

    assert not any(storage.exists(name) for name in picture_names)
    assert not Author.objects.exists()


@pytest.mark.django_db
def test_delete_model_without_file_still_deletes_record(rf, author_admin, caplog):
    author = make_author()  # no attachment

    with caplog.at_level(logging.ERROR):
        author_admin.delete_model(rf.post("/"), author)

    assert not Author.objects.exists()
    assert caplog.text == ""


@pytest.mark.django_db
def test_delete_error_is_logged_and_record_deleted(rf, caplog):
    blog = Blog.objects.create(name="Blog", description="A blog")
    blog_admin = BlogAdmin(Blog, admin.AdminSite())

    # default file_field_names is ["file"], which doesn't exist on Blog
    with caplog.at_level(logging.ERROR):
        blog_admin.delete_model(rf.post("/"), blog)

    assert not Blog.objects.exists()
    assert "Could not delete file on field 'file'" in caplog.text


@pytest.mark.django_db
def test_delete_queryset_error_is_logged_and_records_deleted(rf, caplog):
    for i in range(2):
        Blog.objects.create(name=f"Blog {i}", description="A blog")
    blog_admin = BlogAdmin(Blog, admin.AdminSite())

    with caplog.at_level(logging.ERROR):
        blog_admin.delete_queryset(rf.post("/"), Blog.objects.all())

    assert not Blog.objects.exists()
    assert caplog.text.count("Could not delete file on field 'file'") == 2
