#!/usr/bin/env python
__author__ = "Robertv"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"

from flask_cors import cross_origin
from Pterodactyl.Common.Routing.JSON_Wrap import Basic_Request


class ClusterClassifierRoutes:
    def __init__(self, logger):
        self.logger = logger
        self.klass = "ClusterClassifierRoutes"

    def add_routes(self, app, cluster_classifier_controller):

        @app.route("/v1/clusterClassifier/status", methods=["GET"])
        @cross_origin()
        def cluster_status():
            self.logger.Info(None, self.klass, "add_routes", "Calling analyze")
            return Basic_Request(cluster_classifier_controller.get_status)()

        @app.route("/v1/clusterClassifier/clusters", methods=["GET"])
        @cross_origin()
        def cluster_clusters():
            self.logger.Info(None, self.klass, "add_routes", "Calling analyze")
            return Basic_Request(cluster_classifier_controller.get_clusters)()
