from collections.abc import Callable
from threading import Lock
from typing import Any


def singleton[T](provider_func: Callable[..., T]) -> Callable[..., T]:
    """
    Thread-safe implementation of Singleton. Should be as a decorator of a "provider" function. A "provider" function
    is one which provides an instance of a class.
    Notes:
        The lock in the singleton decorator ensures that only one thread at a time can create an instance. However, it
        does not automatically make the created instance of the underlying class thread-safe!
    """
    providers = {}
    lock = Lock()

    def get_instance(*args: Any, **kwargs: Any) -> T:
        # As multiple threads could access `if cls not in instances` at the same time, this creates a race condition,
        # and we could have two different instances created. By using a lock, only ont thread at a time could execute
        # the check below.
        with lock:
            # if the provider func is not in the dict
            if provider_func not in providers:
                # We set in the dict: the provider type as key, and the provided instance as value
                providers[provider_func] = provider_func(*args, **kwargs)

        # we return the value from the dict (a.k.a the instance of the class)
        return providers[provider_func]

    return get_instance
