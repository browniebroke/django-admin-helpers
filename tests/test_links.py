import pytest

from django_admin_helpers.links import (
    admin_add_url,
    admin_link_tag,
    admin_list_url,
    admin_url,
    inline_button,
    link_tag,
)

from .testapp.models import Author, Blog, Post


@pytest.mark.parametrize(
    ("model_class", "expected_url"),
    [
        (Blog, "/admin/testapp/blog/"),
        (Post, "/admin/testapp/post/"),
        (Author, "/admin/testapp/author/"),
    ],
)
def test_admin_list_url(model_class, expected_url):
    model_url = admin_list_url(model_class)
    instance = model_class()
    instance_url = admin_list_url(instance)
    assert instance_url == model_url == expected_url


def test_admin_list_url_with_setting(settings):
    settings.ADMIN_HELPERS_URL_NAMESPACE = "admin"
    url = admin_list_url(Blog)
    assert url == "/admin/testapp/blog/"


@pytest.mark.parametrize(
    ("model_class", "expected_url"),
    [
        (Blog, "/admin/testapp/blog/add/"),
        (Post, "/admin/testapp/post/add/"),
        (Author, "/admin/testapp/author/add/"),
    ],
)
def test_admin_add_url(model_class, expected_url):
    url = admin_add_url(model_class)
    assert url == expected_url


@pytest.mark.parametrize(
    ("model_class", "expected_url"),
    [
        (Blog, "/admin/testapp/blog/1/change/"),
        (Post, "/admin/testapp/post/1/change/"),
        (Author, "/admin/testapp/author/1/change/"),
    ],
)
def test_admin_url(model_class, expected_url):
    instance = model_class(id=1)
    instance_url = admin_url(instance)
    assert instance_url == expected_url


@pytest.mark.parametrize(
    ("label", "expected_str"),
    [
        (
            None,
            (
                '<a href="/admin/testapp/blog/1/change/">'
                "/admin/testapp/blog/1/change/</a>"
            ),
        ),
        (
            "Blog link",
            '<a href="/admin/testapp/blog/1/change/">Blog link</a>',
        ),
    ],
)
def test_admin_link_tag(label, expected_str):
    actual_str = admin_link_tag(Blog(id=1), label)
    assert str(actual_str) == expected_str


def test_admin_link_tag_no_instance():
    actual_str = admin_link_tag(None, "example")
    assert str(actual_str) == ""


@pytest.mark.parametrize(
    ("url", "label", "blank", "expected_str"),
    [
        (
            "/something/",
            "Link",
            False,
            '<a href="/something/">Link</a>',
        ),
        (
            "https://example.com",
            "External link",
            True,
            '<a href="https://example.com" target="_blank">External link</a>',
        ),
    ],
)
def test_link_tag(url, label, blank, expected_str):
    actual_str = link_tag(url, label, blank)
    assert str(actual_str) == expected_str


@pytest.mark.parametrize(
    ("extra_kwargs", "expected_styles"),
    [
        ({}, "margin-top: 0; margin-bottom: 1rem"),
        ({"mt": "0", "mb": "2rem"}, "margin-top: 0; margin-bottom: 2rem"),
        ({"mt": "1rem", "mb": "0"}, "margin-top: 1rem; margin-bottom: 0"),
    ],
)
def test_inline_button(extra_kwargs, expected_styles):
    actual_str = inline_button("/something/", "Link", **extra_kwargs)
    assert str(actual_str) == (
        "\n"
        '<a href="/something/" class="button"\n'
        f'   style="{expected_styles}; display: inline-block;">\n'
        "    Link\n"
        "</a>\n"
    )
