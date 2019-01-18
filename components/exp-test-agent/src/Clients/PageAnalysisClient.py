import requests
import urllib3
from Pterodactyl.Common.EurekaConnection.DiscoveryHelper import DiscoveryHelper

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PageAnalysisClient:

    ANALYSIS_RUN_URL = "{}v1/pageAnalysis/state/concrete"

    def __init__(self, logger, eureka_session=None):
        self._klass = "PageAnalysisClient"
        self.logger = logger
        self.disc = DiscoveryHelper(eureka_session)
        self.OWNER = "RC"

    def run_analysis(self, context, concrete_state):
        loc = self.disc.root("pterodactyl.pagecomp.analysis.service")
        url = PageAnalysisClient.ANALYSIS_RUN_URL.format(loc)
        self.logger.Info(context, self._klass, "run_analysis", "Running page analysis: {}".format(url))
        resp = requests.post(url, json=concrete_state, verify=False)
        if resp.status_code == 200:
            self.logger.Info(context, self._klass, "run_analysis", "Successfully ran page analysis.")
            resp = resp.json()

            page_titles = len(resp['analysis']['pageTitles'])
            label_candidates = len(resp['analysis']['labelCandidates'])
            error_messages = len(resp['analysis']['errorMessages'])

            resp['analysis']['PAGETITLE'] = resp['analysis']['pageTitles']
            resp['analysis']['LABELCANDIDATE'] = resp['analysis']['labelCandidates']
            resp['analysis']['ERRORMESSAGE'] = resp['analysis']['errorMessages']
            resp['analysis']['COMMIT'] = resp['analysis']['commits']
            resp['analysis']['CANCEL'] = resp['analysis']['cancels']

            if page_titles > 0:
                self.logger.Info(context, self._klass, "run_analysis", "Perceived {} page titles.".format(page_titles))
            if label_candidates > 0:
                self.logger.Info(context, self._klass, "run_analysis", "Perceived {} label candidates.".format(label_candidates))
            if error_messages > 0:
                self.logger.Info(context, self._klass, "run_analysis", "Perceived {} error messages.".format(error_messages))
            return resp
        else:
            self.logger.Error(context, self._klass, "launch", "Unable to run page analysis.")
            return False
