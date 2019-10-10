from typing import Callable


class override:
    def __call__(self, func: Callable):
        func.__doc__ = "this override  method"


class privet:
    def __call__(self, func: Callable, *args, **kwargs):
        func.__doc__ = "this override  method"
