from django_admin_helpers.main import add, is_enabled


def test_add():
    """Adding two number works as expected."""
    assert add(1, 1) == 2


def test_is_enabled_with_default_value():
    """Enabled function works as expected when unset."""
    assert is_enabled() is True


def test_is_enabled_when_overridden(settings):
    """Enabled function works as expected when setting is changed."""
    settings.ADMIN_HELPERS_ENABLED = False
    assert is_enabled() is False
