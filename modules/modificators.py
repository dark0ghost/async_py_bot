from typing import Callable


class override:
    def __call__(self, func: Callable) -> Callable:
        func.__doc__ = "this override  method"
        return func


class private:
    def __call__(self, func: Callable, *args, **kwargs) -> Callable:
        func.__doc__ = "this private  method"
        return func
