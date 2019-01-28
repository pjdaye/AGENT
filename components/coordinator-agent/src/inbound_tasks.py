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

    msg = "Received abstract test on COORDINATOR QUEUE:"

    if planned_hash in processed_tests:
        LOGGER.info(f'{msg} ({str(planned_hash)}) {str(planned_flow.original_flow)}. (DUPLICATE)')
    else:
        LOGGER.info(f'{msg} ({str(planned_hash)}) {str(planned_flow.original_flow)}. (NEW)')
        LOGGER.info('Publishing to round-robin WORKER QUEUE.')

        AgentFlowPublisher.publish(flow_data)
        processed_tests.add(planned_hash)
    return True
