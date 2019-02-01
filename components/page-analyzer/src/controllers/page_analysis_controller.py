"""Responds to page analysis HTTP requests."""

import json

import bottle
from aist_common.log import get_logger
from bottle import request
from services.page_analysis_service import PageAnalysisService

LOGGER = get_logger('page_analysis_controller')


class PageAnalysisController:
    """Responds to page analysis HTTP requests."""

    def __init__(self, app, service=None):
        """ Initializes the PageAnalysisController class.

        :param app: The Bottle app.
        :param service: An instance of the PageAnalysisService class.
        """

        self._app = app
        if service is not None:
            self._service = service
        else:
            self._service = PageAnalysisService()

    def add_routes(self):
        """ Add request routes to the Bottle app.
        """

        self._app.route('/v1/status', method="GET", callback=self.get_status)
        self._app.route('/v1/pageAnalysis/state/concrete', method="POST", callback=self.page_analysis)
        self._app.route('/v1/pageTitleAnalysis/state/concrete', method="POST", callback=self.get_page_titles)
        self._app.route('/v1/pageAnalysis/state/add', method="POST", callback=self.add)

    @staticmethod
    def get_status() -> bottle.HTTPResponse:
        """ Get service status.

        :return: OK status response.
        """

        return bottle.HTTPResponse(body={'status': 'OK'}, status=200)

    def page_analysis(self):
        """ Run page analysis for the POSTed concrete state.

        :return: The page analysis output for the provided concrete state (element classifications).
        """

        results = {}

        concrete_state = json.load(request.body)

        analysis = self._service.get_page_analysis(concrete_state)

        LOGGER.info('Analysis completed...')

        results["analysis"] = analysis

        LOGGER.debug('Results built...')

        return bottle.HTTPResponse(body=results, status=200)

    def get_page_titles(self):
        """ Run page title analysis for the POSTed concrete state.

        :return: The page analysis output for the provided concrete state (element classifications).
        """

        results = {}

        concrete_state = json.load(request.body)

        analysis = self._service.get_page_titles(concrete_state)

        results["analysis"] = analysis

        return bottle.HTTPResponse(body=results, status=200)

    def add(self):
        """ Adds a labeled element to the underlying training data, and retrains the underlying classifiers.

        :return: Response code.
        """

        results = {}

        element = json.load(request.body)

        self._service.add_element(element)

        return bottle.HTTPResponse(body=results, status=200)
