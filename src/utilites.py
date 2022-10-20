from datetime import datetime
from functools import wraps


def timeit(func):
    """
    decorator to measure execution time for PoW.
    """
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = datetime.now()
        res = func(*args, **kwargs)
        print(f'excution time of {func.__name__} is {datetime.now() - start_time}')
        return res
    return timeit_wrapper
