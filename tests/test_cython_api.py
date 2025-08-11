import pytest

CYTHON_API = pytest.importorskip("testcythonapi")


def test_under_cached_property() -> None:
    uc_property = CYTHON_API.TestUnderCachedProperty()
    assert uc_property.prop() == 1
    assert uc_property.prop2() == "foo"


def test_cached_property() -> None:
    c_property = CYTHON_API.TestCachedProperty()
    assert c_property.prop() == 1
    assert c_property.prop2() == "foo"


def test_under_cached_property_assignment() -> None:
    a = CYTHON_API.TestUnderCachedPropertyAssignment()
    with pytest.raises(AttributeError):
        a.prop = 123  # type: ignore[assignment]
