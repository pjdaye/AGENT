import threading
import time
import uuid

import celery.worker
import jsonpickle

from aist_common.CeleryConfig.celery_app import app

worker = celery.worker.WorkController(app=app,
                                      hostname="test-agent-" + uuid.uuid4().hex,
                                      pool_cls='solo',
                                      queues=['test_agent_queue'])

threading.Thread(target=worker.start).start()

global celery_memory
celery_memory = {}

global memory_lock
memory_lock = threading.Lock()

time.sleep(3)


@app.task(name='test_agent.handle_planned_flow', queue="test_agent_queue")
def handle_planned_flow(flow_data):
    planned_flow = jsonpickle.decode(flow_data)
    planned_hash = planned_flow.hash

    print()
    print("RECV: ({}) {}".format(str(planned_hash), str(planned_flow.original_flow)))

    memory_lock.acquire()

    if planned_flow.initial_state.hash not in celery_memory:
        celery_memory[planned_flow.initial_state.hash] = []
    celery_memory[planned_flow.initial_state.hash].append(planned_flow)

    print("Flow Queues:")
    for key, val in celery_memory.items():
        print("State: {}, |Queue|: {}".format(str(key), str(len(val))))

    print()

    memory_lock.release()

    return True


worker.reload()
