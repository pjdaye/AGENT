import json

import bottle
from aist_common.log import get_logger
from bottle import request
from services.page_analysis_service import PageAnalysisService

LOGGER = get_logger('page_analysis_controller')


class PageAnalysisController:
    def __init__(self, app):
        self._app = app
        self._service = PageAnalysisService()

    def add_routes(self):
        self._app.route('/v1/status', method="GET", callback=self.get_status)
        self._app.route('/v1/pageAnalysis/state/concrete', method="POST", callback=self.page_analysis)
        self._app.route('/v1/pageTitleAnalysis/state/concrete', method="POST", callback=self.get_page_titles)
        self._app.route('/v1/pageAnalysis/state/add', method="POST", callback=self.add)

    @staticmethod
    def get_status():
        return bottle.HTTPResponse(body={'status': 'OK'}, status=200)

    def page_analysis(self):
        results = {}

        concrete_state = json.load(request.body)

        analysis = self._service.get_page_analysis(concrete_state)

        LOGGER.info('Analysis completed...')

        results["analysis"] = analysis

        LOGGER.info('Results built...')

        return bottle.HTTPResponse(body=results, status=200)

    def get_page_titles(self):
        results = {}

        concrete_state = json.load(request.body)

        analysis = self._service.get_page_titles(concrete_state)

        results["analysis"] = analysis

        return bottle.HTTPResponse(body=results, status=200)

    def add(self):
        results = {}

        element = json.load(request.body)

        self._service.add_element(element)

        return bottle.HTTPResponse(body=results, status=200)
