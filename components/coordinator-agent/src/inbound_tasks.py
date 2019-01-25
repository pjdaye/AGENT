import jsonpickle
from aist_common.CeleryConfig.celery_app import create_app
from aist_common.log import get_logger

from memory.agent_memory import *
from outbound_tasks import AgentFlowPublisher

LOGGER = get_logger('inbound-tasks')

app = create_app([])


# INBOUND TASKS.

@app.task(name='test_coordinator.handle_planned_flow', queue="test_coordinator_queue")
def coordinator_handle_planned_flow(flow_data):
    planned_flow = jsonpickle.decode(flow_data)
    planned_hash = planned_flow.hash
    if planned_hash in processed_tests:
        print("SKIP: ({}) {}".format(str(planned_hash), str(planned_flow.original_flow)))
    else:
        print("PROC: ({}) {}".format(str(planned_hash), str(planned_flow.original_flow)))
        AgentFlowPublisher.publish(flow_data)
        processed_tests.add(planned_hash)
    return True
