import uuid

from aist_common.CeleryConfig.celery_app import create_app
from aist_common.log import get_logger

LOGGER = get_logger('gateway-service')


class GatewayService:
    @staticmethod
    def start_session(request_payload):
        app = create_app([])

        @app.task(name='test_agent.start_session', queue="agent_broadcast_tasks")
        def start_agent_session(_):
            pass

        session_id = uuid.uuid4().hex
        request = {'SUT_URL': request_payload['SUT_URL']}

        LOGGER.info(f'Signaling agents to start exploring: {request["SUT_URL"]}')

        start_agent_session.delay(request)
        return {'session': session_id}

    @staticmethod
    def stop_session():
        app = create_app([])

        @app.task(name='test_agent.stop_session', queue="agent_broadcast_tasks")
        def stop_agent_session():
            pass

        LOGGER.info(f'Signaling agents to stop exploration.')

        stop_agent_session.delay()
        return {'stopped': True}
