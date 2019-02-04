"""Responds to gateway HTTP requests."""

import bottle
from aist_common.log import get_logger
from bottle import request
from services.gateway_service import GatewayService

LOGGER = get_logger('gateway-controller')


class GatewayController:
    """Responds to gateway HTTP requests."""

    def __init__(self, app):
        """ Initializes the GatewayController class.

        :param app: The Bottle app.
        """

        self._app = app
        self._service = GatewayService()

    def add_routes(self):
        """ Add request routes to the Bottle app.
        """
        self._app.route('/v1/status', method="GET", callback=self.get_status)
        self._app.route('/v1/start', method="POST", callback=self.start_session)
        self._app.route('/v1/stop', method="POST", callback=self.stop_session)

    @staticmethod
    def get_status():
        """ Get service status.

        :return: OK status response.
        """

        return bottle.HTTPResponse(body={'status': 'OK'}, status=200)

    def start_session(self):
        """ Handles a request to start an exploration/testing session.

        :return: The session ID for the newly started session.
        """

        request_payload = request.json
        session = self._service.start_session(request_payload)
        return bottle.HTTPResponse(body=session, status=200)

    def stop_session(self):
        """ Handles a request to stop all running sessions.

        :return: OK if the session stop request was successfully handled.
        """

        response = self._service.stop_session()
        return bottle.HTTPResponse(body=response, status=200)
