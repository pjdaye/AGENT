#!/usr/bin/env python

__author__ = "DionnyS"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"

import time

from Pterodactyl.Common.Logger import Logger, LOG_TRACE
from Pterodactyl.Common.ConfigManager import Configurations, ConfigManager
from Pterodactyl.Common.EurekaConnection.EurekaSession import EurekaSession

from PageAnalysisService.config import ProductionConfig, DevelopmentConfig, TestingConfig

def initialize():
    logger = Logger()
    logger.SetLogLevel(LOG_TRACE)
    configs = Configurations(ProductionConfig, DevelopmentConfig, TestingConfig)
    conf = ConfigManager(configs).current_config()

    started = False
    eureka_session = None


    while not started:
        try:
            eureka_session = EurekaSession(conf, logger)
            eureka_session.register()
            started = True
        except Exception as msg:
            logger.Error(None, "main", "initialize", "Cannot access discovery. {0}".format(msg))
            time.sleep(5)

    eureka_session.heartbeat()

initialize()