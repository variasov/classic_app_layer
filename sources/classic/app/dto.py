from pydantic import BaseModel


class DTO(BaseModel):
    """Base class for DTO with validation"""

    def populate_obj(self, obj, **kwargs):
        if 'exclude_unset' not in kwargs:
            kwargs['exclude_unset'] = True

        for key, value in self.dict(**kwargs).items():
            setattr(obj, key, value)

    def create_obj(self, cls, **kwargs):
        if 'exclude_unset' not in kwargs:
            kwargs['exclude_unset'] = True

        return cls(**self.dict(**kwargs))
