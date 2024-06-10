from django.db import models


class Blog(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    def __str__(self):  # noqa: D105
        return self.name


class Author(models.Model):
    full_name = models.CharField(max_length=50)
    picture = models.ImageField(upload_to="authors")

    def __str__(self):  # noqa: D105
        return self.full_name


class Post(models.Model):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):  # noqa: D105
        return self.title
