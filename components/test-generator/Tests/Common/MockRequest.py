#!/usr/bin/env python

__author__ = "DionnyS"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"

class MockRequest:
    def __init__(self):
        self.parameters = {}
        self.query = {}

    def set_request(self, r):
        self.parameters["request"] = r