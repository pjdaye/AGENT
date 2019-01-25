import requests

from aist_common.log import get_logger

LOGGER = get_logger('runner-client')


class RunnerClient:
    RUNNER_LAUNCH_URL = "{}v1/runner/launch"
    RUNNER_NAVIGATE_URL = "{}v1/runner/navigate"
    RUNNER_CONCRETE_STATE_URL = "{}v1/runner/concreteState?owner={}"
    RUNNER_COMMAND_URL = "{}v1/runner/command"

    def __init__(self, runner_url):
        self._klass = "RunnerClient"
        self.RUNNER_URL = runner_url
        self.OWNER = "RC"

    def launch(self, url):
        body = {
            "ownerFootprint": self.OWNER,
            "url": url
        }
        loc = "https://aistrunner-pythondionny.apps.mia.ulti.io/"
        launch_url = RunnerClient.RUNNER_LAUNCH_URL.format(loc)

        LOGGER.info("Launching runner: {}".format(launch_url))

        resp = requests.post(launch_url, json=body)
        if resp.status_code == 200:
            LOGGER.info("Successfully launched runner.")
            return True
        else:
            LOGGER.error("Unable to launch runner.")
            return False

    def navigate(self, url):
        body = {
            "ownerFootprint": self.OWNER,
            "url": url
        }
        loc = "https://aistrunner-pythondionny.apps.mia.ulti.io/"
        url = RunnerClient.RUNNER_NAVIGATE_URL.format(loc)
        LOGGER.info("Navigating runner: {}".format(url))
        resp = requests.post(url, json=body)
        if resp.status_code == 200:
            LOGGER.info("Successfully navigated runner.")
            return True
        else:
            LOGGER.error("Unable to navigate runner.")
            return False

    def concrete_state(self):
        loc = "https://aistrunner-pythondionny.apps.mia.ulti.io/"
        url = RunnerClient.RUNNER_CONCRETE_STATE_URL.format(loc, self.OWNER)
        LOGGER.info("Grabbing concrete state: {}".format(url))
        resp = requests.get(url)
        if resp.status_code == 200:
            LOGGER.info("Successfully scraped concrete state.")
            return resp.json()
        else:
            LOGGER.error("Unable to scrape concrete state.")
            return False

    def perform_action(self, selector, action, value=None):
        body = {
            "ownerFootprint": self.OWNER,
            "interaction": action,
            "widget": {
                "selector": selector
            },
            "value": value
        }
        loc = "https://aistrunner-pythondionny.apps.mia.ulti.io/"
        url = RunnerClient.RUNNER_COMMAND_URL.format(loc)
        LOGGER.info("Performing action: {} {} {}".format(action, selector, value))
        resp = requests.post(url, json=body)
        if resp.status_code == 200:
            LOGGER.info("Successfully performed action.")
            return True
        else:
            LOGGER.error("Unable to perform action.")
            return False
