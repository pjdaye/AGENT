import os

import bottle
from Controllers.PageAnalysisController import PageAnalysisController
from bottle import run

PORT = os.environ['SERVICE_PORT'] \
    if 'SERVICE_PORT' in os.environ else 8080

app = bottle.app()

PageAnalysisController(app).add_routes()


def start():
    run(app=app, host='localhost', port=PORT)


if __name__ == '__main__':
    start()
