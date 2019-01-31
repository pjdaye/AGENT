"""A client that communicates with and provides the capabilities of the runner service."""
import json
import os
import time

from aeoncloud import get_session_factory
from aeoncloud.exceptions.aeon_session_error import AeonSessionError

from aist_common.log import get_logger

LOGGER = get_logger('runner-client')


class RunnerClient:
    """A client that communicates with and provides the capabilities of the runner service."""

    GET_DOCUMENT_LOC = "return document.location.href;"
    HAS_JQUERY_SCRIPT = "if(window.jQuery) return true; return false;"
    FIX_JQUERY_SCRIPT = "if(window.jQuery && !window.jquery) window.jquery = window.jQuery;"

    def __init__(self, runner_url):
        """ Initializes the RunnerClient class.

        :param runner_url: The URL to the Aeon runner to be used.
        """

        self._klass = "RunnerClient"
        self.RUNNER_URL = runner_url
        self.session = None
        self.aeon = get_session_factory()

        with open(os.path.realpath('./data/stateScraper.js'), 'r') as file:
            scrape_js = f'{file.read()} data=window.aist_scrape(); delete data.elements; return JSON.stringify(data);'
            self.SCRAPE_SCRIPT = scrape_js.replace('\n', ' ')

        with open(os.path.realpath('./data/installJQuery.js'), 'r') as file:
            self.JQUERY_SCRIPT = file.read().replace('\n', ' ')

        with open(os.path.realpath('./data/checkReadyState.js'), 'r') as file:
            self.CHECK_READY_SCRIPT = file.read().replace('\n', ' ')

    def launch(self, url):
        """ Communicates with the runner service to launch a runner session
            and navigate to the SUT URL.

        :param url: The URL to navigate to.

        :return: True if the runner session was successfully launched.
        """

        LOGGER.info("Launching runner: {} to {}".format(self.RUNNER_URL, url))

        try:
            self.session = self.aeon.get_session(request_body={
                'settings': {
                    'aeon.platform.http.url': '{}/api/v1/'.format(self.RUNNER_URL),
                    'aeon.browser': 'Chrome',
                    'aeon.protocol': 'http',
                    'aeon.timeout': 10,
                    'aeon.wait_for_ajax_responses': True,
                }
            })

            LOGGER.info("Successfully launched runner.")

            if not self.navigate(url):
                LOGGER.error("Unable to launch runner.")
                return False

            return True

        except AeonSessionError:
            LOGGER.exception("Unable to launch runner.")
            return False

    def navigate(self, url):
        """ Sends a navigation request to a runner session.

        :param url: The URL to navigate to.

        :return: True if the navigation request succeeded.
        """

        try:
            self.session.execute_command('GoToUrlCommand', [url])

            LOGGER.info("Successfully navigated runner.")
            return True

        except AeonSessionError:
            LOGGER.exception("Unable to navigate runner.")
            return False

    def perform_action(self, selector, action, value=None):
        """ Sends an action request to a runner session.

        :param selector: The selector of the element to be interacted with.
        :param action: The requested interaction (e.g. Click, Set).
        :param value: If the desired interaction is "Set", the value to set the element to.

        :return: True if the action request succeeded.
        """

        try:
            css = {'type': 'jQuery', 'value': selector}
            if action.upper() == 'SET':
                self.session.execute_command('SetCommand', [css, "Text", value])
            elif action.upper() == 'CLICK':
                self.session.execute_command('ClickCommand', [css, "Text", value])

            LOGGER.info(f'Successfully performed action: {action} {selector} {value}')
            return True

        except AeonSessionError:
            LOGGER.exception(f'Unable to perform action: {action} {selector} {value}')
            return False

    def quit(self):
        """ Sends a quit request to a runner session.

        :return: True if the quit request succeeded.
        """

        try:
            self.session.quit_session()

            LOGGER.info("Successfully quit runner.")
            return True

        except AeonSessionError:
            LOGGER.exception("Unable to quit runner.")
            return False

    def concrete_state(self):
        """ Collects the current concrete state of the page that the active runner session is currently on.

        :return: A concrete state.
        """

        try:
            resp = self.session.execute_command('ExecuteScriptCommand', [self.GET_DOCUMENT_LOC])

            if not resp['success']:
                LOGGER.error(f'Failed to scrape concrete state: {resp["failureMessage"]}')
                return False

            if resp['data'].endswith('.xml') or resp['data'].endswith('.json'):
                LOGGER.info("Successfully collected concrete state.")
                return self._get_empty_concrete_state(resp['data'], resp['data'])

            resp = self.session.execute_command('ExecuteScriptCommand', [self.HAS_JQUERY_SCRIPT])

            if not resp['success']:
                LOGGER.error(f'Failed to scrape concrete state: {resp["failureMessage"]}')
                return False

            has_jquery = resp['data'] == 'true'

            if not has_jquery:
                resp = self.session.execute_command('ExecuteAsyncScriptCommand', [self.JQUERY_SCRIPT])

            if not resp['success']:
                LOGGER.error(f'Failed to scrape concrete state: {resp["failureMessage"]}')
                return False

            resp = self.session.execute_command('ExecuteScriptCommand', [self.FIX_JQUERY_SCRIPT])

            if not resp['success']:
                LOGGER.error(f'Failed to scrape concrete state: {resp["failureMessage"]}')
                return False

            dom_loaded = self._is_dom_loaded()

            if not dom_loaded:
                LOGGER.error("Unable to verify DOM was loaded.")
                return False

            resp = self.session.execute_command('ExecuteScriptCommand', [self.SCRAPE_SCRIPT])

            if not resp['success']:
                LOGGER.error(f'Failed to scrape concrete state: {resp["failureMessage"]}')
                return False

            state_json = json.loads(resp['data'])
            LOGGER.info("Successfully collected concrete state.")
            return state_json

        except AeonSessionError:
            LOGGER.exception("Unable to scrape concrete state.")
            return False

    @staticmethod
    def _get_empty_concrete_state(url, title):
        """ Constructs a concrete state that has a title and URL, but no widgets.

        :param url: The URL to assign to the concrete state.
        :param title: The title to assign to the concrete state.

        :return: A concrete state.
        """

        return {
            "url": url,
            "title": title,
            "widgets": {},
            "root": "HTML0_0:0"
        }

    def _is_dom_loaded(self):
        """ Checks for browser document ready state.

        :return: True if the browser document has completed loading.
        """

        LOGGER.info('Checking for DOM ready state...')
        attempts = 0
        dom_loaded = False

        while attempts < 10:
            resp = self.session.execute_command('ExecuteAsyncScriptCommand', [self.CHECK_READY_SCRIPT])

            if not resp['success']:
                LOGGER.error(f'Failed to wait for DOM ready state: {resp["failureMessage"]}')
                return False

            dom_loaded = resp['data'] == 'true'

            if dom_loaded:
                break

            time.sleep(0.2)

        return dom_loaded
