#!/usr/bin/env python
from PageAnalysisService.Services.PageAnalysisService import PageAnalysisService

__author__ = "DionnyS"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"


import json
import http.client
from Pterodactyl.Common.Logger import Verbose
from ACL.ACL import ACL
from ACL.ACLClient import ACLClient


class PageAnalysisController():
    OK = "ok"

    def __init__(self, logger, config, eureka_session):
        self.logger = logger
        self.c_name = self.__class__.__name__
        self.service = PageAnalysisService(ACL(ACLClient(eureka_session=eureka_session)))

    def Hello(self):
        doc = {}
        doc["name"] = "PageAnalysis"
        return (doc, self.OK)

    @Verbose()
    def analyze(self, context):
        self.logger.depth = 1
        results = {}
        status = "OK"
        status_code = http.client.OK

        concrete_state = context.get_parameter("request")

        analysis = self.service.get_page_analysis(context, concrete_state)

        results["analysis"] = analysis

        return results, status, status_code

    @Verbose()
    def get_page_titles(self, context):
        self.logger.depth = 1
        results = {}
        status = "OK"
        status_code = http.client.OK

        concrete_state = context.get_parameter("request")

        analysis = self.service.get_page_titles(context, concrete_state)

        results["analysis"] = analysis

        return results, status, status_code

    @Verbose()
    def add(self, context):
        self.logger.depth = 1
        results = {}
        status = "OK"
        status_code = http.client.OK

        element = context.get_parameter("request")

        self.service.add_element(context, element)

        return results, status, status_code
