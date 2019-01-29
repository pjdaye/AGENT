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
    NUM_ITERATIONS = 1000

    def __init__(self, sut_url, runner_url):
        self.sut_url = sut_url
        self.runner_url = runner_url

        self.mapper = StateAbstracter()
        self.ext_labels = LabelExtraction()
        self.aide = AIDEMock()
        self.memory = PriorityMemory()
        self.observer = StateObserver()
        self.seq_parser = SequenceParser()
        self.flow_plan = FlowPlanner(self.aide)
        self.defect_rep = DefectReporter()
        self.flow_publish = PlannedFlowPublisher()

        self.web_driver = RunnerClient(self.runner_url)
        self.web_classifier = PageAnalysisClient()
        self.flow_generator = FlowGeneratorClient()

        self.flow_exec = FlowExecutor(self.aide,
                                      self.web_classifier,
                                      self.mapper,
                                      self.ext_labels,
                                      self.observer,
                                      self.defect_rep)

    def start(self):
        loop_thread = threading.Thread(target=self._loop_start)
        loop_thread.start()

    def _loop_start(self):
        launched = self.web_driver.launch(self.sut_url)

        if not launched:
            return

        for i in range(AgentLoop.NUM_ITERATIONS):
            LOGGER.info(f"Starting loop iteration {str(i)}.")

            # noinspection PyBroadException
            try:
                self._loop_iteration()
            except Exception:
                LOGGER.exception(f"Fatal error during iteration {str(i)}.")
                LOGGER.info(f"Stopping session.")
                break

        self._loop_end()

    def _loop_end(self):
        self.web_driver.quit()

    def _loop_iteration(self):
        concrete_state = self.web_driver.concrete_state()

        if concrete_state is False:
            raise Exception("Error during session.")

        page_analysis = self.web_classifier.run_analysis(concrete_state)

        act_state = self.mapper.process(concrete_state)

        LOGGER.info("Arrived at state: {}.".format(act_state.hash))

        self.ext_labels.extract_labels(act_state, page_analysis)

        if len(act_state.widgets) == 0:
            LOGGER.info("No actionable widgets found. Restarting session.")
            self.web_driver.navigate(self.sut_url)
            return

        '''
            We've arrived to a new actionable state.  Run through the following algorithm:
            1) perceive the environment.  For all actionable widgets, list observations.
            2) Query the flow generator for possible test flows given the observations.
            3) For each flow:
                a) Execute the flow.
                b) Report possible defects.
        '''

        observations = self.observer.perceive(act_state, page_analysis)
        test_flow_queue = []

        for observation in observations:
            LOGGER.info("Perceived: {}".format(str(observation)))
            generated_flow = self.flow_generator.generate_flow(str(observation))
            if generated_flow is not None and generated_flow is not False:
                LOGGER.info("Generated flow: {}".format(generated_flow))
                parsed_flow = self.seq_parser.parse(generated_flow)
                if parsed_flow:
                    planned_flows = self.flow_plan.plan(act_state, page_analysis, parsed_flow)
                    if planned_flows is not False:
                        test_flow_queue.extend(planned_flows)

        if len(test_flow_queue) > 0:
            for planned_flow in test_flow_queue:
                self.flow_publish.publish(planned_flow)

        memory_lock.acquire()
        if act_state.hash in celery_memory:
            test_execution_queue = celery_memory[act_state.hash]
            if len(test_execution_queue) > 0:
                planned_flow_to_execute = test_execution_queue.pop(0)
                planned_flow_to_execute.calculate_hash()

                LOGGER.info(f'De-queued abstract test off from WORKER QUEUE: {planned_flow_to_execute.hash}')

                memory_lock.release()
                self.flow_exec.execute(act_state, self.web_driver, planned_flow_to_execute)
                return
            else:
                memory_lock.release()
        else:
            memory_lock.release()

        # If we're here, we didn't execute a flow.  Are there any?
        if len(test_flow_queue) > 0:

            LOGGER.info("No abstract tests on WORKER QUEUE. Executing first available abstract test.")

            is_ok = self.flow_exec.execute(act_state, self.web_driver, test_flow_queue[0])

            if not is_ok:
                raise Exception("Unable to execute flow step.")

            return

        if self.memory.in_memory(act_state.hash):
            chosen_widget = self.memory.choose_widget(act_state)
        else:
            chosen_widget = self.memory.choose_randomly(act_state)

        self.memory.update_memory(act_state, chosen_widget)

        if len(chosen_widget["actions"]) == 0:
            LOGGER.info("No actions found on widget: {}. Skipping.".format(chosen_widget["key"]))
            return

        action = random.choice(chosen_widget["actions"])

        value = None

        if action == 'set':
            value = self.aide.get_concrete_value(chosen_widget['label'])
            pass

        LOGGER.info("Performing action {} on widget {}.".format(action, chosen_widget["key"]))

        ok = self.web_driver.perform_action(chosen_widget["selector"], action, value)

        if not ok:
            LOGGER.info("Unable to perform action.")
