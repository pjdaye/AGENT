import bottle
from aist_common.log import get_logger
from bottle import request, response
from services.gateway_service import GatewayService

LOGGER = get_logger('gateway-controller')


class GatewayController:
    def __init__(self, app):
        self._app = app
        self._service = GatewayService()

    def add_routes(self):
        self._app.route('/v1/status', method="GET", callback=self.get_status)
        self._app.route('/v1/start', method="POST", callback=self.start_session)
        self._app.route('/v1/stop', method="POST", callback=self.stop_session)

    @staticmethod
    def get_status():
        return bottle.HTTPResponse(body={'status': 'OK'}, status=200)

    def start_session(self):
        request_payload = request.json
        LOGGER.info(f'Starting session: {request_payload}')
        session = self._service.start_session(request_payload)
        return bottle.HTTPResponse(body=session, status=200)

    def stop_session(self):
        LOGGER.info(f'Stopping session')
        session = self._service.stop_session()
        return bottle.HTTPResponse(body=session, status=200)
