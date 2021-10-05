# Classic App Layer

This package provides primitives for application layer.
Part of project "Classic".

Usage for validation:

```python
from dataclasses import dataclass

from classic.app import DTO, validate_with_dto
from pydantic import validate_arguments


class SomeDTO(DTO):
    """Based on pydantic.BaseModel. Used for validating input"""
    
    some_field: int
    another_field: str


@dataclass
class SomeAppCls:
    """Some class with app logic. May be mapped on DB."""
    some_field: int
    another_field: str


class SomeService:
    
    @validate_arguments
    def some_method(self, arg: int):
        assert isinstance(arg, int)
    
    @validate_with_dto
    def another_method(self, params: SomeDTO):
        instance = params.create_obj(SomeAppCls)
        print(instance)

```

Usage for errors:
```python
from classic.app import AppError, ErrorsList


# Describe errors, possible in application
class IncorrectState(AppError):
    msg_template = 'Incorrect app state - "{text}"'
    code = 'app.incorrect_state'


class ServiceNotReady(AppError):
    msg_template = 'Service not ready yet'
    code = 'app.service_not_ready'


# In another file with services:
class SomeService:
    
    def __init__(self):
        self.ready_to_serve = False

    def is_ready(self):
        """Demonstrates simple usage"""
        if not self.ready_to_serve:
            raise ServiceNotReady()

    def mark_as_ready(self):
        """Demonstrates usage of error message templates"""
        if self.ready_to_serve:
            raise IncorrectState(text='Service are ready')
        self.ready_to_serve = True

    def just_give_errors(self):
        """Demonstrates method, what may have more than 1 error"""
        errors = [IncorrectState(text='error 1'), 
                  IncorrectState(text='error 2')]
        raise ErrorsList(errors)


# Somewhere in adapters:

service = SomeService()

try:
    service.is_ready()
except AppError as error:
    print(f'Application responses with error code "{error.code}", '
          f'message is "{error.message}"')

try:
    service.mark_as_ready()
    service.mark_as_ready()
except AppError as error:
    print(f'Application responses with error code "{error.code}", '
          f'message is "{error.message}"')
    
try:
    service.just_give_errors()
except ErrorsList as errors_list:
    for error in errors_list.errors:
        print(f'Application responses with error code "{error.code}", '
              f'message is "{error.message}"')
```
