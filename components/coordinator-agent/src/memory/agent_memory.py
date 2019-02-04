"""Shared memory that is read and written to by all executing threads within a single coordinator agent."""

import threading

global processed_tests
processed_tests = set([])

global memory_lock
memory_lock = threading.Lock()
