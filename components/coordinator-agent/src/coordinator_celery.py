import threading
import time

import celery.worker
import jsonpickle

from aist_common.CeleryConfig.celery_app import app

worker = celery.worker.WorkController(app=app,
                                      hostname="test-coordinator",
                                      pool_cls='solo',
                                      queues=['test_coordinator_queue'])

threading.Thread(target=worker.start).start()

global processed_tests
processed_tests = set([])


@app.task(name='test_agent.handle_planned_flow', queue="test_agent_queue")
def agent_handle_planned_flow(_):
    pass


@app.task(name='test_coordinator.handle_planned_flow', queue="test_coordinator_queue")
def coordinator_handle_planned_flow(flow_data):
    planned_flow = jsonpickle.decode(flow_data)
    planned_hash = planned_flow.hash
    if planned_hash in processed_tests:
        print("SKIP: ({}) {}".format(str(planned_hash), str(planned_flow.original_flow)))
    else:
        print("PROC: ({}) {}".format(str(planned_hash), str(planned_flow.original_flow)))
        agent_handle_planned_flow.delay(flow_data)
        processed_tests.add(planned_hash)
    return True


time.sleep(1)
worker.reload()
