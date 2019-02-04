"""Contains all outbound Celery tasks."""

from aist_common.CeleryConfig.celery_app import create_app

app = create_app([])


# OUTBOUND TASKS.

@app.task(name='test_agent.handle_planned_flow', queue="test_agent_queue")
def agent_handle_planned_flow(_):
    """ An external Celery task (Worker Agent) responsible for consuming queued concrete test flows.
    """
    pass


class AgentFlowPublisher:
    """Responsible for publishing concrete test flows."""

    @staticmethod
    def publish(flow_data):
        """ Publishes a concrete test flow to a task queue consumed by the Coordinator Agent.

        :param flow_data: The concrete test flow data to publish.
        """

        agent_handle_planned_flow.delay(flow_data)
