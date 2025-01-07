import functools
import time

from loguru import logger


def logging(*, on_entry=True, on_exit=True, timeit=True, level="DEBUG"):
    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)

            if timeit:
                start_time = time.perf_counter()
            if on_entry:
                logger_.log(level, "Entering '{}'", name)
            result = func(*args, **kwargs)
            if on_exit:
                logger_.log(level, "Exiting '{}'", name)
            if timeit:
                end_time = time.perf_counter()
                logger_.log(level, "Elapsed time of '{}': {:.6f}s", name, end_time - start_time)
            return result

        return wrapped

    return wrapper
