import jsonpickle

from src.CeleryConfig import app


@app.task(name='test_coordinator.handle_planned_flow', queue="test_coordinator_queue")
def coordinator_handle_planned_flow(_):
    pass


class PlannedFlowPublisher:
    def __init__(self):
        pass

    @staticmethod
    def publish(planned_flow):
        planned_flow.calculate_hash()
        json_out = jsonpickle.encode(planned_flow)
        coordinator_handle_planned_flow.delay(json_out)
