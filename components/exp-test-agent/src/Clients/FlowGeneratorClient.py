import requests
import urllib3
from Pterodactyl.Common.EurekaConnection.DiscoveryHelper import DiscoveryHelper

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class FlowGeneratorClient:

    FLOW_GEN_URL = "{}v1/testSequence/predict"

    def __init__(self, logger, eureka_session=None):
        self._klass = "FlowGeneratorClient"
        self.logger = logger
        self.disc = DiscoveryHelper(eureka_session)
        self.OWNER = "RC"

    def generate_flow(self, context, query):
        loc = self.disc.root("pterodactyl.pagecomp.analysis.service")
        url = FlowGeneratorClient.FLOW_GEN_URL.format(loc)
        self.logger.Info(context, self._klass, "generate_flow", "Running flow generator: {}, {}".format(url, query))
        query = [flow_step.lower() for flow_step in query.split(' ')]
        resp = requests.post(url, json=query, verify=False)

        if resp.status_code == 200:
            self.logger.Info(context, self._klass, "generate_flow", "Successfully ran flow generator.")
            resp = resp.json()
            sequences = resp['sequences']
            if len(sequences) > 0:
                sequence = sequences[0]
                expanded_sequence = " ".join(sequence).upper()
                self.logger.Info(context, self._klass, "generate_flow", "Generated flow: {}".format(expanded_sequence))
                return expanded_sequence
            return None
        else:
            self.logger.Error(context, self._klass, "generate_flow", "Unable to run flow generator.")
            return False
