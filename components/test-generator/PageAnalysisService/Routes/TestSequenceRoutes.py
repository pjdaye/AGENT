#!/usr/bin/env python

__author__ = "DionnyS"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"

from flask_cors import cross_origin
from Pterodactyl.Common.Routing.JSON_Wrap import JSON_Request


class TestSequenceRoutes:
    def __init__(self, logger):
        self.logger = logger
        self.klass = "TestSequenceRoutes"

    def add_routes(self, app, test_sequence_controller):

        @app.route("/v1/testSequence/predict", methods=["POST"])
        @cross_origin()
        def test_sequence_predict():
            self.logger.Info(None, self.klass, "add_routes", "Calling test sequence predict")
            return JSON_Request(test_sequence_controller.predict)()

        @app.route("/v1/testSequence/predictMany", methods=["POST"])
        @cross_origin()
        def test_sequence_predict_many():
            self.logger.Info(None, self.klass, "add_routes", "Calling test sequence predict")
            return JSON_Request(test_sequence_controller.predict_many)()
