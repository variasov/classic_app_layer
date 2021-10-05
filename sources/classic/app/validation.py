from functools import wraps
import inspect

from .dto import DTO

__all__ = ['validate_with_dto']


def _validate_signature_length(parameters):
    # TODO: Needed another, more stable way for detecting methods and functions
    #  inspect.ismethod works only on instances, not on class functions
    needed_len = 2 if 'self' in parameters else 1

    params_len = len(parameters)
    return params_len == needed_len


def _get_last_param(parameters):
    # We need to take last key in dict,
    # but can't do dict.keys()[-1]
    name = next(reversed(parameters.keys()))
    return parameters[name]


def validate_with_dto(function):
    """
    Decorator for function and methods, what receiving one parameter - DTO.
    """
    signature = inspect.signature(function)

    assert _validate_signature_length(signature.parameters), \
        f'Callable, decorated by validate_with_dto, ' \
        f'must have only 1 parameter!'

    dto_param = _get_last_param(signature.parameters)
    assert issubclass(dto_param.annotation, DTO), \
        f'Argument of {function} must be a DTO! ' \
        f'Argument {dto_param.name} is {dto_param.annotation}'

    dto_cls = dto_param.annotation

    @wraps(function)
    def wrapper(*args, **kwargs):
        # TODO: args passed to target function for working with methods
        #  If wrapped function will be called with any args, args will be passed
        #  to target function. Validation of args number in decorator
        #  prevents it, but this looks ugly
        return function(*args, dto_cls(**kwargs))

    setattr(wrapper, '__annotations__', dto_cls.__annotations__)

    return wrapper
