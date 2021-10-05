from dataclasses import dataclass

from classic.app import DTO


class SomeDTO(DTO):
    int_field: int
    str_field: str = None


@dataclass
class SomeCls:
    int_field: int
    str_field: str = None


def test_populate_obj():
    dto = SomeDTO(int_field=1)
    instance = SomeCls(0, 'abc')

    dto.populate_obj(instance)

    assert instance.int_field == 1
    assert instance.str_field == 'abc'


def test_create_obj():
    dto = SomeDTO(int_field=1)

    instance = dto.create_obj(SomeCls)

    assert instance.int_field == 1
    assert instance.str_field is None
