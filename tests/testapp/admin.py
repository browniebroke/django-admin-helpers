from django.contrib import admin
from testapp.models import Author, Blog, Post


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("full_name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title",)
