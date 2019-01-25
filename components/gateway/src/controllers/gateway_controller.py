import bottle
from aist_common.log import get_logger
from bottle import request
from services.gateway_service import GatewayService

LOGGER = get_logger('gateway-controller')


class GatewayController:
    def __init__(self, app):
        self._app = app
        self._service = GatewayService()

    def add_routes(self):
        self._app.route('/v1/status', method="GET", callback=self.get_status)
        self._app.route('/v1/start', method="POST", callback=self.start_session)

    @staticmethod
    def get_status():
        return bottle.HTTPResponse(body={'status': 'OK'}, status=200)

    def start_session(self):
        request_payload = request.json
        session = self._service.start_session(request_payload)
        return bottle.HTTPResponse(body=session, status=200)
