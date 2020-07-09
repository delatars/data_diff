import pytest

from data_diff.bases import BaseLoader
from data_diff.loaders import (
    Excell,
    Gsheet
)


test_loaders = (
    Excell,
    Gsheet,
)


@pytest.fixture(scope="function", params=test_loaders)
def parameters_test(request):
    return request.param


def test_subclass(parameters_test):
    loader = parameters_test
    assert issubclass(loader, BaseLoader), f"{loader.__name__}: is not subclass of 'BaseLoader'"


def test_attributes(parameters_test):
    loader = parameters_test
    methods = [
        "__iter__",
        "__next__",
        "delete",
        "update",
        "close",
    ]
    properties = {
        "name": str,
        "schemes": (tuple, list),
        "uri_example": str,
    }
    for attr in methods:
        try:
            method = getattr(loader, attr)
            assert callable(method), f"{attr} - Not callable"
        except (AttributeError, AssertionError) as ex:
            raise AssertionError(f"{loader.__name__}: {ex}") from None

    for prop, dtype in properties.items():
        try:
            attr = getattr(loader, prop)
            assert isinstance(attr, dtype), f"{prop} - Not of type: {dtype}"
        except (AttributeError, AssertionError) as ex:
            raise AssertionError(f"{loader.__name__}: {ex}") from None


def test_uri_example(parameters_test):
    loader = parameters_test
    if "{scheme}" not in loader.uri_example:
        raise AssertionError(f"{loader.__name__}: 'uri_example' should contain '{{scheme}}' formatting pattern")
