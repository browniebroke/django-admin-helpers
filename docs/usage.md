(usage)=

# Usage

Assuming that you've followed the {ref}`installations steps <installation>`, you're now ready to use this package. It provides a collection of functions to quickly and easily build hyperlinks into the admin.

For example, let say you have a `BlogPost` model that has a link to an `Author` model:

```python
class Author(models.Model):
    full_name = models.CharField(max_length=50)

    def __str__(self):  # noqa: D105
        return self.full_name


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    def __str__(self):
        return self.title
```

Now you may want to show the list of posts in the admin, and show their respective authors:

```python
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "author"]
    list_select_related = ["author"]
```

Without this package, if you want to turn the author column into a link to the author admin page, you may do:

```python
from django.urls import reverse
from django.utils.html import format_html


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "_author_link"]
    list_select_related = ["author"]

    @admin.display(label="Author")
    def _author_link(self, post):
        author = post.author
        app_label = author._meta.app_label
        model_name = author._meta.model_name
        url = reverse(f"admin:{app_label}_{model_name}_change")
        return format_html(
             '<a href="{url}">{label}</a>',
            url=url,
            label=str(author)
        )
```

This quite a bit of boilerplate! You could simplify it and hardcode some pieces, but you may trade-off some robustness.

Here is how it look with django-admin-helpers:

```python
from django_admin_helpers.links import admin_url


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "_author_link"]
    list_select_related = ["author"]

    @admin.display(label="Author")
    def _author_link(self, post):
        return admin_url(post.author)
```

You need to add the method, and it's pretty explicit what's happening and where the URL comes from.

Ready to dive in? Check out the {ref}`next section <reference>` about the full API or {ref}`the configuration options <configuration>` available.
