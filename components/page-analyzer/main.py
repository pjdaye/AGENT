import os

import bottle
from bottle import run

from page_analysis_service.controllers.page_analysis_controller import PageAnalysisController


PORT = os.environ['SERVICE_PORT'] \
    if 'SERVICE_PORT' in os.environ else 8080

app = bottle.app()
PageAnalysisController(app).add_routes()

def main():
    run(app=app, host='localhost', port=PORT)

if __name__ == '__main__':
    main()
