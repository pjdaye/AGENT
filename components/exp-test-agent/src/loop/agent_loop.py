""" Responsible for implementing the core control flow of the agent.
        Observes the SUT environment, plans, and acts upon the environment."""

import random

from aide.aide_mock import AIDEMock
from aist_common.grammar.sequence_parser import SequenceParser
from abstraction.state_abstracter import StateAbstracter
from clients.flow_generation_client import FlowGeneratorClient
from clients.page_analysis_client import PageAnalysisClient
from clients.runner_client import RunnerClient
from defects.defect_reporter import DefectReporter
from flow_execution.flow_executor import FlowExecutor
from flow_execution.flow_planner import FlowPlanner
from memory.priority_memory import PriorityMemory
from outbound_tasks import PlannedFlowPublisher
from perceive.label_extraction import LabelExtraction
from perceive.state_observer import StateObserver
from aist_common.log import get_logger

from memory.agent_memory import *

LOGGER = get_logger('agent-loop')


class AgentLoop:
    """ Responsible for implementing the core control flow of the agent.
        Observes the SUT environment, plans, and acts upon the environment."""

    NUM_ITERATIONS = 1000

    def __init__(self, sut_url, runner_url):
        """ Initializes the AgentLoop class.

        :param sut_url: The URL of the SUT.
        :param runner_url: The URL to the runner resource to be used for driving the SUT.
        """

        self.sut_url = sut_url
        self.runner_url = runner_url

        self.mapper = StateAbstracter()
        self.label_extracter = LabelExtraction()
        self.form_expert = AIDEMock()
        self.memory = PriorityMemory()
        self.observer = StateObserver()
        self.seq_parser = SequenceParser()
        self.flow_planner = FlowPlanner()
        self.defect_rep = DefectReporter()
        self.flow_publish = PlannedFlowPublisher()

        self.runner = RunnerClient(self.runner_url)
        self.page_analyzer = PageAnalysisClient()
        self.flow_generator = FlowGeneratorClient()

        self.flow_executer = FlowExecutor(self.form_expert,
                                          self.page_analyzer,
                                          self.mapper,
                                          self.label_extracter,
                                          self.observer,
                                          self.defect_rep)

    def start(self):
        """ Starts the agent control loop.
        """

        loop_thread = threading.Thread(target=self._loop_start)
        loop_thread.start()

    def _loop_start(self):

        """ Runs the main control loop.
            Starts by launching the runner, then executes AgentLoop.NUM_ITERATIONS loop iterations.

        :return: Returns once execution has finalized. Also returns if the runner is unable to be launched.
        """

        launched = self.runner.launch(self.sut_url)

        if not launched:
            return

        for i in range(AgentLoop.NUM_ITERATIONS):
            LOGGER.info(f"Starting loop iteration {str(i)}.")

            if general_memory['SESSION_STOPPED']:
                LOGGER.info(f"Stopping session due to user stop request.")
                break

            # noinspection PyBroadException
            try:
                self._loop_iteration()
            except Exception:
                LOGGER.exception(f"Fatal error during iteration {str(i)}.")
                LOGGER.info(f"Stopping session.")
                break

        self._loop_end()

    def _loop_end(self):
        """ Finalizes the main control loop, closing any open runner session.
        """

        self.runner.quit()

    def _loop_iteration(self):
        """ Executes a single control loop iteration. Each loop iteration performs the following steps:
            1) Perceive the current environment, drawing observations.
            2) For each observation, consult the flow generation service to generate abstract test flows.
            3) For each generated abstract flow, attempt to map it to one or more concrete test flows for the SUT.
            4) Publish all concrete test flows to a message queue to be consumed by the Coordinator Agent.
            5) If there exists a concrete test flow on our work queue (populated by the Coordinator Agent)
                that is currently executable based on current SUT context, pop it off the queue and execute it.
            6) Otherwise, check if there is an executable test flow that resulted from Step 3. If so, execute it.
            7) Otherwise, go into exploration mode.

        :return:
        """

        """First, observe the current environment, extracting information necessary to make a decision."""
        concrete_state = self.runner.concrete_state()

        if concrete_state is False:
            raise Exception("Error during session.")

        page_analysis = self.page_analyzer.run_analysis(concrete_state)
        abstract_state = self.mapper.process(concrete_state)

        LOGGER.info("Arrived at state: {}.".format(abstract_state.hash))

        self.label_extracter.extract_labels(abstract_state, page_analysis)

        if len(abstract_state.widgets) == 0:
            LOGGER.info("No actionable widgets found. Restarting session.")
            self.runner.navigate(self.sut_url)
            return

        """
            We've arrived to a new actionable state.  Run through the following algorithm:
            1) Perceive the environment.  For all actionable widgets, list observations.
            2) Query the flow generator for possible test flows given the observations.
            3) For each flow:
                a) Execute the flow.
                b) Report possible defects.
        """

        observations = self.observer.perceive(abstract_state, page_analysis)

        """ 
            Observations are constructed via the ML-based element classifiers, 
            and are in natural language form (e.g. Observe TextBox FirstName)
        """

        test_flow_queue = []

        for observation in observations:
            LOGGER.info("Perceived: {}".format(str(observation)))

            """Generated test flows are also in natural language form."""
            generated_flow = self.flow_generator.generate_flow(str(observation))

            if generated_flow is not None and generated_flow is not False:
                LOGGER.info("Generated flow: {}".format(generated_flow))

                """Parse the generated flow, constructing an AST leveraging our grammar."""
                parsed_flow = self.seq_parser.parse(generated_flow)

                if parsed_flow:

                    """Leverage the flow planner to convert the abstract flow into concrete flows."""
                    planned_flows = self.flow_planner.plan(abstract_state, page_analysis, parsed_flow)

                    if planned_flows is not False:

                        """Extend the internal concrete test flow queue with any planned flows."""
                        test_flow_queue.extend(planned_flows)

        """Publish all planned flows to the Coordinator Agent."""
        if len(test_flow_queue) > 0:
            for planned_flow in test_flow_queue:
                self.flow_publish.publish(planned_flow)

        """ Consume any concrete test flows that have been put on our 
            Celery-based worker queue by the Coordinator Agent. """

        memory_lock.acquire()
        if abstract_state.hash in celery_memory:
            test_execution_queue = celery_memory[abstract_state.hash]
            if len(test_execution_queue) > 0:
                planned_flow_to_execute = test_execution_queue.pop(0)
                planned_flow_to_execute.calculate_hash()

                LOGGER.info(f'De-queued abstract test off from WORKER QUEUE: {planned_flow_to_execute.hash}')

                memory_lock.release()
                self.flow_executer.execute(abstract_state, self.runner, planned_flow_to_execute)

                """End the iteration if we've executed a concrete test flow."""
                return
            else:
                memory_lock.release()
        else:
            memory_lock.release()

        """If we're here, we didn't execute a flow.  Are there any on our own internal queue?"""

        if len(test_flow_queue) > 0:

            LOGGER.info("No abstract tests on WORKER QUEUE. Executing first available abstract test.")

            is_ok = self.flow_executer.execute(abstract_state, self.runner, test_flow_queue[0])

            if not is_ok:
                raise Exception("Unable to execute flow step.")

            """End the iteration if we've executed a concrete test flow."""
            return

        """If we're here, we still have not executed a flow. Go into EXPLORATION mode."""

        if self.memory.in_memory(abstract_state.hash):
            chosen_widget = self.memory.choose_widget(abstract_state)
        else:
            chosen_widget = self.memory.choose_randomly(abstract_state)

        self.memory.update_memory(abstract_state, chosen_widget)

        if len(chosen_widget["actions"]) == 0:
            LOGGER.info("No actions found on widget: {}. Skipping.".format(chosen_widget["key"]))
            return

        action = random.choice(chosen_widget["actions"])

        value = None

        if action == 'set':

            if chosen_widget['label'] is None:
                LOGGER.warning(f"Attempting to set widget ${chosen_widget['key']}, but no widget label found.")
                return

            value = self.form_expert.get_concrete_value(chosen_widget['label'])
            pass

        LOGGER.info("Performing action {} on widget {}.".format(action, chosen_widget["key"]))

        ok = self.runner.perform_action(chosen_widget["selector"], action, value)

        if not ok:
            LOGGER.info("Unable to perform action.")
