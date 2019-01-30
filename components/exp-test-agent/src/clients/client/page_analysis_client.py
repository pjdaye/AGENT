import os

import requests
import urllib3

from aist_common.log import get_logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGGER = get_logger('page-analysis-client')


class PageAnalysisClient:

    ANALYSIS_RUN_URL = "{}/v1/pageAnalysis/state/concrete"

    def __init__(self):
        self._klass = "PageAnalysisClient"
        self._set_envs()

    def _set_envs(self):
        self.SERVICE_URL = 'http://page-analyzer'
        if 'PAGE_ANALYSIS_URL' in os.environ:
            self.SERVICE_URL = os.environ['PAGE_ANALYSIS_URL']

    def run_analysis(self, concrete_state):
        url = PageAnalysisClient.ANALYSIS_RUN_URL.format(self.SERVICE_URL)

        LOGGER.info("Running page analysis: {}".format(url))

        resp = requests.post(url, json=concrete_state, verify=False)
        if resp.status_code == 200:
            LOGGER.info("Successfully ran page analysis.")
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
                LOGGER.info("Perceived {} page titles.".format(page_titles))
            if label_candidates > 0:
                LOGGER.info("Perceived {} label candidates.".format(label_candidates))
            if error_messages > 0:
                LOGGER.info("Perceived {} error messages.".format(error_messages))
            return resp
        else:
            LOGGER.error("Unable to run page analysis.")
            return False
