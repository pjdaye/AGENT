#!/usr/bin/env python

__author__ = "DionnyS"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"

from Pterodactyl.Common.EurekaConnection.DiscoveryHelper import DiscoveryHelper
from Pterodactyl.Common.Logger import Logger


class ACLClient:
    def __init__(self, eureka_session=None):
        self.logger = Logger()
        self.disc = DiscoveryHelper(eureka_session)

    def get_data(self, context, version_id):
        return []
