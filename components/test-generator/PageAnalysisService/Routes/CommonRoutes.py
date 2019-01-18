#!/usr/bin/env python

__author__ = "DionnyS"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"

from Pterodactyl.Common.Routing.ErrorHandler import APIError
from flask import jsonify
from flask_cors import cross_origin


class CommonRoutes():

    def add_common_routes(self, app, page_analysis_controller):
        @app.after_request
        def add_header(response):
            response.headers["PageCompRouting-Domain-ID"] = 'PageAnalysis-1.0'
            return response

        @app.errorhandler(APIError)
        def handle_invalid_usage(error):
            response = jsonify(error.to_dict())
            response.status_code = error.status_code
            return response

        @app.route("/info", methods=["GET"])
        @cross_origin()
        def info():
            return jsonify({'Response': 'PageAnalysis Service'})