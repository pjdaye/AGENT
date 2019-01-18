#!/usr/bin/env python

__author__ = "DionnyS"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"

import json

import jsonpickle


class Create:
    @staticmethod
    def __encoding(obj: object, dictionary):
        dictionary["py/object"] = obj.__module__ + "." + obj.__name__
        return dictionary

    @staticmethod
    def __decoded_obj(obj: object, dictionary):
        dictionary = Create.__encoding(obj, dictionary)
        return jsonpickle.decode(json.dumps(dictionary))

    # @staticmethod
    # def label(label, confidence):
    #     label_dict = {
    #         "label": label,
    #         "confidence": confidence
    #     }
    #     return Create.__encoding(Label, label_dict)
