"""A client that communicates with and provides the capabilities of the page analysis service."""
import os

import requests
import urllib3

from aist_common.log import get_logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGGER = get_logger('page-analysis-client')


class PageAnalysisClient:
    """A client that communicates with and provides the capabilities of the page analysis service."""

    ANALYSIS_RUN_URL = "{}/v1/pageAnalysis/state/concrete"

    def __init__(self):
        """ Initializes the PageAnalysisClient class.
        """

        self._klass = "PageAnalysisClient"
        self._set_envs()

    def _set_envs(self):
        """ Loads environment variables.
        """

        self.SERVICE_URL = 'http://page-analyzer'
        if 'PAGE_ANALYSIS_URL' in os.environ:
            self.SERVICE_URL = os.environ['PAGE_ANALYSIS_URL']

    def run_analysis(self, concrete_state):
        """ Communicates with the page analysis service to run machine learning classifiers
            on the current concrete state for the purpose of element classification.

        :param concrete_state: The concrete state to run analysis on.

        :return: Classified elements.
        """

        url = PageAnalysisClient.ANALYSIS_RUN_URL.format(self.SERVICE_URL)

        LOGGER.info("Running page analysis: {}".format(url))

        resp = requests.post(url, json=concrete_state, verify=False)
        if resp.status_code == 200:
            LOGGER.debug("Successfully ran page analysis.")
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
                LOGGER.debug("Perceived {} page titles.".format(page_titles))
            if label_candidates > 0:
                LOGGER.debug("Perceived {} label candidates.".format(label_candidates))
            if error_messages > 0:
                LOGGER.debug("Perceived {} error messages.".format(error_messages))
            return resp
        else:
            LOGGER.error("Unable to run page analysis.")
            return False
