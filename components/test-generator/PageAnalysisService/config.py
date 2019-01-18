#!/usr/bin/env python

__author__ = "DionnyS"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"

from Pterodactyl.Common.ConfigManager import BaseConfig


class PageAnalysisConfig(BaseConfig):
    SERVICE_NAME=BaseConfig.PAGE_COMP_PAGE_ANALYSIS_SERVICE_NAME
    SERVICE_HOST="192.168.99.100"
    SERVICE_PORT=9007
    MONGO_DB = "PageAnalysis"

    PCF_SPACE = "production"
    MONGO_HOST = '10.50.17.173'
    EUREKA_HOST = "pterodactyleureka" + PCF_SPACE + ".apps.mia.ulti.io/"

    #Cluster Classifier Configuration
    MAX_ITERATIONS = 10

    # To use TTL on configurations, set CHECKPOINT_TTL in the environment
    # docker image.  This time should be an integer number of seconds
    BaseConfig.RECONFIGURABLES.append("CHECKPOINT_TTL")
    CHECKPOINT_TTL = None

class ProductionConfig(PageAnalysisConfig):
    DEBUG = False


class DevelopmentConfig(PageAnalysisConfig):
    DEVELOPMENT = True
    DEBUG = True
    MONGO_HOST = '192.168.99.100:27017'


class TestingConfig(PageAnalysisConfig):
    TESTING = True
    DEBUG = True
    MONGO_HOST = '192.168.99.100:27017'
    MONGO_DB = "PageAnalysis_test"
