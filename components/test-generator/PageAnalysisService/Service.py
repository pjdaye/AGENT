#!/usr/bin/env python
from PageAnalysisService.Controllers.TestSequenceController import TestSequenceController

__author__ = "DionnyS"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"

import time

from Pterodactyl.Common.ConfigManager import ConfigManager, Configurations, BaseConfig
from Pterodactyl.Common.EurekaConnection.EurekaSession import EurekaSession
from Pterodactyl.Common.Logger import Logger
from Pterodactyl.Common.Routing.ErrorHandler import ErrorRouter
from Pterodactyl.Common.Routing.ServiceDiscoveryRoutes import DiscoveryRoutes

from flask import Flask
from flask_cors import CORS

from PageAnalysisService.config import ProductionConfig, DevelopmentConfig, TestingConfig
from PageAnalysisService.Routes.CommonRoutes import CommonRoutes

from PageAnalysisService.Controllers.PageAnalysisController import PageAnalysisController
from PageAnalysisService.Routes.PageAnalysisRoutes import PageAnalysisRoutes

from PageAnalysisService.Controllers.ClusterClassifierController import ClusterClassifierController
from PageAnalysisService.Routes.ClusterClassifierRoutes import ClusterClassifierRoutes
from PageAnalysisService.Routes.TestSequenceRoutes import TestSequenceRoutes


def config_ssl_context(config):
    if config.USE_SSL:
        cert_dir = "/Users/davida/Projects/pterodactyl/lib/certs"
        cert = cert_dir + "/pterodactyl-cert.pem"
        key = cert_dir + "/pterodactyl-key.pem"
        context = (cert, key)
        return context
    else:
        return None


def initialize():
    logger = Logger()
    app = Flask(__name__)
    cors = CORS(app)

    configs = Configurations(ProductionConfig, DevelopmentConfig, TestingConfig)
    config = ConfigManager(configs).current_config()

    app.config.from_object(config)
    app.config['CORS_HEADERS'] = 'Content-Type'

    started = False
    eureka_session = None

    while not started:
        try:
            eureka_session = EurekaSession(config, logger)
            started = True
        except Exception as msg:
            logger.Error(None, "main", "initialize", "Cannot access eureka. {0}".format(msg))
            time.sleep(5)


    ErrorRouter().add_error_routes(app)
    discovery_routes = DiscoveryRoutes(eureka_session, logger)
    discovery_routes.add_discovery_routes(app)

    page_analysis_controller = PageAnalysisController(logger, config, eureka_session=eureka_session)
    CommonRoutes().add_common_routes(app, page_analysis_controller)
    PageAnalysisRoutes(logger).add_routes(app, page_analysis_controller)

    cluster_classifier_controller = ClusterClassifierController(logger, config, eureka_session=eureka_session)
    ClusterClassifierRoutes(logger).add_routes(app, cluster_classifier_controller)

    test_sequence_controller = TestSequenceController(logger, config, eureka_session=eureka_session)
    TestSequenceRoutes(logger).add_routes(app, test_sequence_controller)

    return app, config

app, conf = initialize()

if __name__ == "__main__":
    ssl_context = config_ssl_context(conf)
    app.run(processes=8, host="0.0.0.0", port=conf.SERVICE_PORT, ssl_context=ssl_context)
    # app.run(host="0.0.0.0")
