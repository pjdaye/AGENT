import os
import hashlib

from PageAnalysisService.config import ProductionConfig
from Pterodactyl.Common.Logger import Logger
from Pterodactyl.Common.EurekaConnection.EurekaSession import EurekaSession

from PageAnalysisService.Services.ClusterClassifier.StateReader import StateDataProvider
from PageAnalysisService.Services.ClusterClassifier.Checkpointer import Checkpointer
from PageAnalysisService.Services.ClusterClassifier.Classifier import ClusterStateClassifier

# Data Directories for the ClusterClassifier
HOME_DIR = "/Users/robertv"
DATA_DIR = os.path.join(HOME_DIR, "Downloads/Datasets/Ptero/RecStates")

DOMAIN_DIR = os.path.join(HOME_DIR, "UltiProjects/AutoTester/pterodactyl/domains/pageComp")
APP_DIR = os.path.join(DOMAIN_DIR, "pageAnalysis/PageAnalysisService/Services/ClusterClassifier")
checkpoint_folder = os.path.join(APP_DIR, "Checkpoints")

VERSION_ID = "5ad3e829099fa30027e4a38e"
K = 50

def main():
    cfg = ProductionConfig()
    logger = Logger()
    eureka_session = EurekaSession(cfg, logger)
    context = None
    cfg.STATE_DATA_FILE_DIR = DATA_DIR
    cfg.CHECKPOINT_DIR = checkpoint_folder

    data_provider = StateDataProvider(logger, cfg, eureka_session, VERSION_ID)
    data = data_provider.read_data()

    checkpointer = Checkpointer(cfg, VERSION_ID, K, data)
    c = ClusterStateClassifier(logger, cfg, K, checkpointer)
    c.get_clusters(context, data)
    c.show_stats()

    # from PageAnalysisService.Services.ClusterClassifier.Visualizer import DistanceVisualizer
    # dv = DistanceVisualizer(data)
    # dv.show_distances(c)
    #
    # from PageAnalysisService.Services.ClusterClassifier.Visualizer import ScreenShotVisualizer
    # sv = ScreenShotVisualizer(c.clusters[9077472515444840285])
    # sv.show_screenshots(data_provider)
    # sv.compare_screenshots(data_provider, 9077472515444840285, -3458861185337882842)

if __name__ == "__main__":
    main()
