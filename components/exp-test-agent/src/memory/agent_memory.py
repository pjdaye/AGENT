import threading

global celery_memory
celery_memory = {}

global memory_lock
memory_lock = threading.Lock()