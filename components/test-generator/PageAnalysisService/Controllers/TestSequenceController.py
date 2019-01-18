#!/usr/bin/env python

__author__ = "DionnyS"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"

import http.client
from Pterodactyl.Common.Logger import Verbose
from ACL.ACL import ACL
from ACL.ACLClient import ACLClient
from PageAnalysisService.Services.TestSequenceService import TestSequenceService


class TestSequenceController():
    OK = "ok"

    def __init__(self, logger, config, eureka_session):
        self.logger = logger
        self.c_name = self.__class__.__name__
        self.service = TestSequenceService(ACL(ACLClient(eureka_session=eureka_session)))

    def Hello(self):
        doc = {}
        doc["name"] = "TestSequence"
        return (doc, self.OK)

    @Verbose()
    def predict(self, context):
        self.logger.depth = 1
        results = {}
        status = "OK"
        status_code = http.client.OK

        query = context.get_parameter("request")

        generated = self.service.predict(context, query, 1)

        generated = self.remove_conseq_dupes(generated)

        results["sequences"] = generated

        return results, status, status_code

    @Verbose()
    def predict_many(self, context):
        self.logger.depth = 1
        results = {}
        status = "OK"
        status_code = http.client.OK

        query = context.get_parameter("request")

        num_to_predict = context.get_parameter("N")

        generated = self.service.predict(context, query, int(num_to_predict))

        generated = self.remove_conseq_dupes(generated)

        results["sequences"] = generated

        return results, status, status_code

    @staticmethod
    def remove_conseq_dupes(generated):
        output = []
        for seq in generated:
            new_seq = []
            for i in range(len(seq)):
                curr = seq[i]
                if i > 0:
                    prev = seq[i - 1]
                if i == 0:
                    new_seq.append(curr)
                else:
                    if curr == prev:
                        continue
                    new_seq.append(curr)
            output.append(new_seq)
        return output

