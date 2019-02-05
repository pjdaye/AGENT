"""Contains all inbound Celery tasks."""

import os
import jsonpickle

from aist_common.CeleryConfig.celery_app import create_app
from aist_common.log import get_logger

from memory.agent_memory import *
from loop.agent_loop import AgentLoop

LOGGER = get_logger('inbound-tasks')

app = create_app([])


# INBOUND TASKS.

@app.task(name='test_agent.start_session', queue="agent_broadcast_tasks")
def start_session(session_start_data):
    """ A Celery task that starts an agent session.

    :param session_start_data: The request payload.
    :return: False if environment variable RUNNER_URL not setup properly; otherwise, True.
    """

    LOGGER.info("Starting session.")

    sut_url = session_start_data['SUT_URL']

    if 'RUNNER_URL' not in os.environ:
        error = "Agent has not been configured with a web runner. Please set the RUNNER_URL environment variable."
        LOGGER.error(error)
        return error

    runner_url = os.environ['RUNNER_URL']

    general_memory['SESSION_STOPPED'] = False

    AgentLoop(sut_url, runner_url).start()

    return True


@app.task(name='test_agent.stop_session', queue="agent_broadcast_tasks")
def stop_session():
    """ A Celery task that stops all agent sessions.

    :return: True
    """

    LOGGER.info("Stopping session.")

    general_memory['SESSION_STOPPED'] = True

    return True


@app.task(name='test_agent.handle_planned_flow', queue="test_agent_queue")
def handle_planned_flow(flow_data):
    """ A Celery task that handles a queued planned concrete test flow (received from the Coordinator Agent).

    :param flow_data: The concrete test flow payload.
    :return: True
    """

    planned_flow = jsonpickle.decode(flow_data)
    planned_hash = planned_flow.hash

    LOGGER.info(f'Received abstract test on WORKER QUEUE.')
    LOGGER.debug(f'({str(planned_hash)}) {str(planned_flow.original_flow)}.')

    memory_lock.acquire()

    if planned_flow.initial_state.hash not in celery_memory:
        celery_memory[planned_flow.initial_state.hash] = []
    celery_memory[planned_flow.initial_state.hash].append(planned_flow)

    LOGGER.debug("Flow Queues:")

    for key, val in celery_memory.items():
        LOGGER.debug(f'State: {str(key)}, |Queue|: {str(len(val))}')

    memory_lock.release()

    return True
