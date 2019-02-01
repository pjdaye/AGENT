"""Contains all outbound Celery tasks."""

import jsonpickle

from aist_common.CeleryConfig.celery_app import create_app

app = create_app([])


# OUTBOUND TASKS.

@app.task(name='test_coordinator.handle_planned_flow', queue="test_coordinator_queue")
def coordinator_handle_planned_flow(_):
    """ An external Celery task (Coordinator Agent) responsible for consuming queued concrete test flows.
    """
    pass


class PlannedFlowPublisher:
    """Responsible for publishing concrete test flows."""

    @staticmethod
    def publish(concrete_flow):
        """ Publishes a concrete test flow to a task queue consumed by the Coordinator Agent.

        :param concrete_flow: The concrete test flow to publish.
        """

        concrete_flow.calculate_hash()
        json_out = jsonpickle.encode(concrete_flow)
        coordinator_handle_planned_flow.delay(json_out)
