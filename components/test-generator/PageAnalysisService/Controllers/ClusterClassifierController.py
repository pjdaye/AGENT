#!/usr/bin/env python
__author__ = "RobertV"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"

from http import HTTPStatus
from Pterodactyl.Common.Logger import Verbose

from PageAnalysisService.Services.ClusterClassifier.ClusterClassifierService import ClusterClassifierService


class ClusterClassifierController:
    OK = "ok"

    def __init__(self, logger, config, eureka_session):
        self.logger = logger
        self.c_name = self.__class__.__name__
        self.service = ClusterClassifierService(logger, config, eureka_session)

    @Verbose()
    def get_clusters(self, context):
        self.logger.depth = 1
        results = {}
        status = "OK"
        status_code = HTTPStatus.OK

        version_id = context.query["version_id"]
        if "K" in context.query:
            K = int(context.query["K"])
        else:
            K = 50

        clusters = self.service.get_clusters(context, version_id, K=K)
        if clusters is None:
            return "Version not found", "BAD VERSION", HTTPStatus.NOT_FOUND

        j_clusters = {}
        for cluster_hash in clusters:
            cluster = clusters[cluster_hash]
            j_cluster = {}
            j_cluster["center"] = self.state_to_JSON(cluster.center)
            j_cluster["members"] = []
            for member in cluster.members:
                j_cluster["members"].append(self.state_to_JSON(member))
            j_clusters[cluster.center.hash] = j_cluster
        results["clusters"] = j_clusters

        return results, status, status_code

    def state_to_JSON(self, state):
        j_state = {}
        j_state["id"] = state.graph_id
        j_state["graph_id"] = state.graph_id
        j_state["hash"] = state.hash
        j_state["name"] = state.name
        j_state["title"] = state.title
        return j_state


    @Verbose()
    def get_status(self, context):
        results = {}
        results["status"] = "Status is OK"
        return results, "OK", HTTPStatus.OK
