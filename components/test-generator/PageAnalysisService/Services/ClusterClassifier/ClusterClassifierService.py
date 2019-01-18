__author__ = "RobertV"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"

import os

from PageAnalysisService.Services.ClusterClassifier.StateReader import StateDataProvider
from PageAnalysisService.Services.ClusterClassifier.Classifier import ClusterStateClassifier
from PageAnalysisService.Services.ClusterClassifier.Checkpointer import Checkpointer


class ClusterClassifierService:
    def __init__(self, logger, cfg, eureka_session):
        self.logger = logger
        self.cfg = cfg
        self.eureka_sesson = eureka_session

    def get_clusters(self, context, version_id, K):
        data_provider = StateDataProvider(self.logger, self.cfg, self.eureka_sesson, version_id)
        data = data_provider.read_data()
        if len(data) < 1 :
            return None

        K = max(K, 50)
        K = max(K, len(data))

        checkpointer = Checkpointer(self.cfg, version_id, K, data)

        c = ClusterStateClassifier(self.logger, self.cfg, K, checkpointer)
        c.get_clusters(context, data)
        return c.clusters
