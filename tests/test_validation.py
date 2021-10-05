import pytest
from pydantic import ValidationError

from classic.app import DTO, validate_with_dto


class SomeDTO(DTO):
    some_field: int


@validate_with_dto
def some_func(params: SomeDTO):
    return params.some_field


class SomeClass:

    @validate_with_dto
    def some_method(self, params: SomeDTO):
        return params.some_field


def test_validate_on_functions():
    with pytest.raises(ValidationError):
        some_func(some_field='abc')

    assert some_func(some_field=1) == 1


def test_validate_on_methods():
    instance = SomeClass()

    with pytest.raises(ValidationError):
        instance.some_method(some_field='abc')

    assert instance.some_method(some_field=1) == 1
