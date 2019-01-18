import json
from http import HTTPStatus

from Services.PageAnalysisService import PageAnalysisService
from bottle import request


class PageAnalysisController:
    def __init__(self, app):
        self._app = app
        self._service = PageAnalysisService()

    def add_routes(self):
        self._app.route('/v1/status', method="GET", callback=self.get_status)
        self._app.route('/v1/pageAnalysis/state/concrete', method="POST", callback=self.page_analysis)
        self._app.route('/v1/pageTitleAnalysis/state/concrete', method="POST", callback=self.get_page_titles)
        self._app.route('/v1/pageAnalysis/state/add', method="POST", callback=self.add)

    def get_status(self):
        return json.dumps({'status': 'OK'})

    def page_analysis(self):
        results = {}
        status = "OK"
        status_code = HTTPStatus.OK

        concrete_state = json.load(request.body)

        analysis = self._service.get_page_analysis(concrete_state)

        results["analysis"] = analysis

        return results, status, status_code

    def get_page_titles(self):
        results = {}
        status = "OK"
        status_code = HTTPStatus.OK

        concrete_state = json.load(request.body)

        analysis = self._service.get_page_titles(concrete_state)

        results["analysis"] = analysis

        return results, status, status_code

    def add(self):
        results = {}
        status = "OK"
        status_code = HTTPStatus.OK

        element = json.load(request.body)

        self._service.add_element(element)

        return results, status, status_code
