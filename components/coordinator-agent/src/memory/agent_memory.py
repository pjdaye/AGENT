import threading

global processed_tests
processed_tests = set([])

global memory_lock
memory_lock = threading.Lock()
