import requests
from Pterodactyl.Common.EurekaConnection.DiscoveryHelper import DiscoveryHelper


class RunnerClient:
    RUNNER_LAUNCH_URL = "{}v1/runner/launch"
    RUNNER_NAVIGATE_URL = "{}v1/runner/navigate"
    RUNNER_CONCRETE_STATE_URL = "{}v1/runner/concreteState?owner={}"
    RUNNER_COMMAND_URL = "{}v1/runner/command"

    def __init__(self, logger, pcf=None, eureka_session=None):
        self._klass = "RunnerClient"
        self.logger = logger
        self.disc = DiscoveryHelper(eureka_session)
        self.RUNNER_PCF = pcf
        self.OWNER = "RC"

    def __prepare_headers(self):
        headers = {
        }
        if self.RUNNER_PCF:
            headers['X-CF-APP-INSTANCE'] = self.RUNNER_PCF
        return headers

    def launch(self, context, url):
        body = {
            "ownerFootprint": self.OWNER,
            "url": url
        }
        # loc = self.disc.root("pterodactyl.runner.service")
        loc = "https://aistrunner-pythondionny.apps.mia.ulti.io/"
        launch_url = RunnerClient.RUNNER_LAUNCH_URL.format(loc)
        self.logger.Info(context, self._klass, "launch", "Launching runner: {}".format(launch_url))
        resp = requests.post(launch_url, json=body, headers=self.__prepare_headers())
        if resp.status_code == 200:
            self.logger.Info(context, self._klass, "launch", "Successfully launched runner.")
            return True
        else:
            self.logger.Error(context, self._klass, "launch", "Unable to launch runner.")
            return False

    def navigate(self, context, url):
        body = {
            "ownerFootprint": self.OWNER,
            "url": url
        }
        # loc = self.disc.root("pterodactyl.runner.service")
        loc = "https://aistrunner-pythondionny.apps.mia.ulti.io/"
        url = RunnerClient.RUNNER_NAVIGATE_URL.format(loc)
        self.logger.Info(context, self._klass, "navigate", "Navigating runner: {}".format(url))
        resp = requests.post(url, json=body, headers=self.__prepare_headers())
        if resp.status_code == 200:
            self.logger.Info(context, self._klass, "navigate", "Successfully navigated runner.")
            return True
        else:
            self.logger.Error(context, self._klass, "navigate", "Unable to navigate runner.")
            return False

    def concrete_state(self, context):
        # loc = self.disc.root("pterodactyl.runner.service")
        loc = "https://aistrunner-pythondionny.apps.mia.ulti.io/"
        url = RunnerClient.RUNNER_CONCRETE_STATE_URL.format(loc, self.OWNER)
        self.logger.Info(context, self._klass, "concrete_state", "Grabbing concrete state: {}".format(url))
        resp = requests.get(url, headers=self.__prepare_headers())
        if resp.status_code == 200:
            self.logger.Info(context, self._klass, "concrete_state", "Successfully scraped concrete state.")
            return resp.json()
        else:
            self.logger.Error(context, self._klass, "concrete_state", "Unable to scrape concrete state.")
            return False

    def perform_action(self, context, selector, action, value=None):
        body = {
            "ownerFootprint": self.OWNER,
            "interaction": action,
            "widget": {
                "selector": selector
            },
            "value": value
        }
        # loc = self.disc.root("pterodactyl.runner.service")
        loc = "https://aistrunner-pythondionny.apps.mia.ulti.io/"
        url = RunnerClient.RUNNER_COMMAND_URL.format(loc)
        self.logger.Info(context, self._klass, "perform_action",
                         "Performing action: {} {} {}".format(action, selector, value))
        resp = requests.post(url, json=body, headers=self.__prepare_headers())
        if resp.status_code == 200:
            self.logger.Info(context, self._klass, "perform_action", "Successfully performed action.")
            return True
        else:
            self.logger.Error(context, self._klass, "perform_action", "Unable to perform action.")
            return False
