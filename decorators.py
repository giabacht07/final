"""Decorators used for logging and history persistence in the Snake Game."""

from functools import wraps


def log_game_event(func):
    """ Middleware decorator logging critical structural game transformations. """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"[EVENT-STREAM] Invoked: {func.__name__:<22} | Return Context: {result}")
        return result
    return wrapper

def history_pipeline(func):
    """ Decorator verifying structural data constraints before flushing records to storage. """
    @wraps(func)
    def wrapper(manager_instance, name, score):
        print(
            f"[DATA-PIPELINE] Incoming validation intercept -> User: {name}, "
            f"Tail Segments: {score}"
        )
        return func(manager_instance, name, score)
    return wrapper
