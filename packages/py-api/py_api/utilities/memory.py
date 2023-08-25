
from os import getpid

from psutil import Process


def get_current_memory_usage_in_mbs() -> float:
    process_id = getpid()
    process = Process(process_id)
    memory: float = process.memory_info().rss

    return memory / (1024 ** 2)
