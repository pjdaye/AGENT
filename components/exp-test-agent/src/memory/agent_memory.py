"""Shared memory that is read and written to by all executing threads within a single worker agent."""

import threading

global celery_memory
celery_memory = {}

global memory_lock
memory_lock = threading.Lock()

global session_stop
session_stop = False