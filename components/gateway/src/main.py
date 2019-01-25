import os

import bottle
from bottle import run

from controllers.gateway_controller import GatewayController


PORT = os.environ['SERVICE_PORT'] \
    if 'SERVICE_PORT' in os.environ else 8080

app = bottle.app()
GatewayController(app).add_routes()


def main():
    run(app=app, host='localhost', port=PORT)


if __name__ == '__main__':
    main()
