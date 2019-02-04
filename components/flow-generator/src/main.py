"""The main service entry-point. Contains all necessary Bottle plumbing code."""

import os

import bottle
from bottle import run
from controllers.test_generator_controller import TestGeneratorController

PORT = os.environ['SERVICE_PORT'] \
    if 'SERVICE_PORT' in os.environ else 8080

app = bottle.app()
TestGeneratorController(app).add_routes()


def main():
    run(app=app, host='localhost', port=PORT)


if __name__ == '__main__':
    main()
