#!/usr/bin/env python

__author__ = "DionnyS"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"

from flask_cors import cross_origin
from Pterodactyl.Common.Routing.JSON_Wrap import JSON_Request


class PageAnalysisRoutes:
    def __init__(self, logger):
        self.logger = logger
        self.klass = "PageAnalysisRoutes"

    def add_routes(self, app, page_analysis_controller):

        @app.route("/v1/pageAnalysis/state/concrete", methods=["POST"])
        @cross_origin()
        def page_analysis():
            self.logger.Info(None, self.klass, "add_routes", "Calling analyze")
            return JSON_Request(page_analysis_controller.analyze)()

        @app.route("/v1/pageTitleAnalysis/state/concrete", methods=["POST"])
        @cross_origin()
        def page_title_analysis():
            self.logger.Info(None, self.klass, "add_routes", "Calling analyze")
            return JSON_Request(page_analysis_controller.get_page_titles)()

        @app.route("/v1/pageAnalysis/state/add", methods=["POST"])
        @cross_origin()
        def add_element():
            print("ASDSADS")
            self.logger.Info(None, self.klass, "add_routes", "Calling analyze")
            return JSON_Request(page_analysis_controller.add)()