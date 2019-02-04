import os

from aist_common.log import get_logger
import bottle
from bottle import run, response

from controllers.gateway_controller import GatewayController

LOGGER = get_logger('gateway-main')

class EnableCors(object):
    LOGGER.info(f'Enabling Cors')
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors

PORT = os.environ['SERVICE_PORT'] \
    if 'SERVICE_PORT' in os.environ else 8080

app = bottle.app()
GatewayController(app).add_routes()

app.install(EnableCors())

def main():
    run(app=app, host='localhost', port=PORT)


if __name__ == '__main__':
    main()
