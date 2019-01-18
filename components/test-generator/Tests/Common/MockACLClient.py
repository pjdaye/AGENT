#!/usr/bin/env python
import jsonpickle

__author__ = "DionnyS"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"

from Pterodactyl.Common.Logger import Logger
import json


class MockACLClient:
    def __init__(self, eureka_session=None, mock_json='DataModel_CandidateName.json'):
        self.logger = Logger()

        with open('LanguageModelResponse.json') as json_data:
            self.__language_model_json = json_data.read()

        with open(mock_json) as json_data:
            self.__data_model_json = json_data.read()

    def get_data_model(self, context, version_id):
        return jsonpickle.decode(self.__data_model_json)

    def get_language_model(self, context, version_id):
        return jsonpickle.decode(self.__language_model_json)
