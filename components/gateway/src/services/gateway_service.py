"""Acts a single entry-point to all other services, handling requests and routing accordingly to other services."""

import uuid

from aist_common.CeleryConfig.celery_app import create_app
from aist_common.log import get_logger

LOGGER = get_logger('gateway-service')


class GatewayService:
    """Acts a single entry-point to all other services, handling requests and routing accordingly to other services."""

    @staticmethod
    def start_session(request_payload):
        """ Handles a request to start an exploration/testing session.

        :param request_payload: A payload which contains the information necessary to start a session.

        :return: The session ID for the newly started session.
        """

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
        """ Handles a request to stop all running sessions.

        :return: A flag indicating that all services were stopped.
        """

        app = create_app([])

        @app.task(name='test_agent.stop_session', queue="agent_broadcast_tasks")
        def stop_agent_session():
            pass

        LOGGER.info(f'Signaling agents to stop exploration.')

        stop_agent_session.delay()
        return {'stopped': True}
