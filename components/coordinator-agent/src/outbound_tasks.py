from aist_common.CeleryConfig.celery_app import create_app

app = create_app([])


# OUTBOUND TASKS.

@app.task(name='test_agent.handle_planned_flow', queue="test_agent_queue")
def agent_handle_planned_flow(_):
    pass


class AgentFlowPublisher:
    def __init__(self):
        pass

    @staticmethod
    def publish(flow_data):
        agent_handle_planned_flow.delay(flow_data)
