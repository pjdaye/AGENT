import random

import os

from Pterodactyl.Common.ConfigManager import Configurations, BaseConfig, ConfigManager
from Pterodactyl.Common.Context import Context
from Pterodactyl.Common.EurekaConnection.EurekaSession import EurekaSession

from AIDE.AIDEMock import AIDEMock
from Abstraction.StateAbstracter import StateAbstracter
from Clients.FlowGeneratorClient import FlowGeneratorClient
from Clients.PageAnalysisClient import PageAnalysisClient
from Clients.RunnerClient import RunnerClient
from Defects.DefectReporter import DefectReporter
from FlowExecution.FlowExecutor import FlowExecutor
from FlowExecution.FlowPlanner import FlowPlanner
from Grammar.SequenceParser import SequenceParser
from Logging.logger import Logger
from Memory.PriorityMemory import PriorityMemory
from Perceive.LabelExtraction import LabelExtraction
from Perceive.StateObserver import StateObserver
from PlannedFlowPublisher import PlannedFlowPublisher

from agent_celery import *


context = Context()
logger = Logger()
mapper = StateAbstracter()
ext_labels = LabelExtraction()
aide = AIDEMock()
memory = PriorityMemory()
observer = StateObserver()
seq_parser = SequenceParser()
flow_plan = FlowPlanner(logger, aide)
defect_rep = DefectReporter()
flow_publish = PlannedFlowPublisher()

SUT_URL = "http://192.168.99.1:8080"
RUNNER_PCF = None
EUREKA_SESSION = None

NUM_ITERATIONS = 1000

if 'SUT_URL' in os.environ:
    SUT_URL = os.environ['SUT_URL']

if 'RUNNER_PCF' in os.environ:
    RUNNER_PCF = os.environ['RUNNER_PCF']

if 'EUREKA_HOST' in os.environ:
    EUREKA_HOST = os.environ['EUREKA_HOST']
    configs = Configurations(BaseConfig())
    config = ConfigManager(configs).current_config()
    EUREKA_SESSION = EurekaSession(config, logger)


_klass = "Agent"

rc = RunnerClient(logger, pcf=RUNNER_PCF, eureka_session=EUREKA_SESSION)
pac = PageAnalysisClient(logger, eureka_session=EUREKA_SESSION)
fgen = FlowGeneratorClient(logger, eureka_session=EUREKA_SESSION)

flow_exec = FlowExecutor(logger, aide, pac, mapper, ext_labels, observer, defect_rep)

launched = rc.launch(context, SUT_URL)

if not launched:
    raise Exception("Unable to start session.")

for i in range(NUM_ITERATIONS):
    concrete_state = rc.concrete_state(context)

    if concrete_state is False:
        raise Exception("Error during session.")

    page_analysis = pac.run_analysis(context, concrete_state)

    act_state = mapper.process(context, concrete_state)

    logger.Info(context, _klass, "Main", "Arrived at state: {}.".format(act_state.hash))

    ext_labels.extract_labels(act_state, page_analysis)

    if len(act_state.widgets) == 0:
        logger.Info(context, _klass, "Main", "No actionable widgets found. Restarting session.")
        rc.navigate(context, SUT_URL)
        continue

    '''
        We've arrived to a new actionable state.  Run through the following algorithm:
        1) Perceive the environment.  For all actionable widgets, list observations.
        2) Query the flow generator for possible test flows given the observations.
        3) For each flow:
            a) Execute the flow.
            b) Report possible defects.
    '''

    web_classifier = None
    web_driver = None
    page_abstraction = None
    flow_publisher = None
    flow_executor = None

    while True:
        concrete_state = web_driver.concrete_state(context)
        page_analysis = web_classifier.run_analysis(context, concrete_state)
        act_state = page_abstraction.process(context, concrete_state)
        observations = observer.perceive(act_state, page_analysis)
        test_flow_queue = []

        for observation in observations:
            generated_flow = fgen.generate_flow(context, str(observation))
            if generated_flow is not False:
                parsed_flow = seq_parser.parse(generated_flow)
                if parsed_flow:
                    planned_flows = flow_plan.plan(context, act_state, page_analysis, parsed_flow)
                    if planned_flows is not False:
                        test_flow_queue.extend(planned_flows)

        for planned_flow in test_flow_queue:
            flow_publisher.publish(planned_flow)

        if len(test_execution_queue) > 0:
            planned_flow_to_execute = test_execution_queue.pop(0)
            flow_executor.execute(context, act_state, rc, planned_flow_to_execute)


    memory_lock.acquire()
    if act_state.hash in celery_memory:
        test_execution_queue = celery_memory[act_state.hash]
        if len(test_execution_queue) > 0:
            planned_flow_to_execute = test_execution_queue.pop(0)
            memory_lock.release()
            flow_exec.execute(context, act_state, rc, planned_flow_to_execute)
            continue
        else:
            memory_lock.release()
    else:
        memory_lock.release()

    # If we're here, we didn't execute a flow.  Are there any?
    if len(test_flow_queue) > 0:
        flow_exec.execute(context, act_state, rc, test_flow_queue[0])
        continue

    if memory.in_memory(act_state.hash):
        chosen_widget = memory.choose_widget(act_state)
    else:
        chosen_widget = memory.choose_randomly(act_state)

    memory.update_memory(act_state, chosen_widget)

    if len(chosen_widget["actions"]) == 0:
        logger.Info(context, _klass, "Main", "No actions found on widget: {}. Skipping.".format(chosen_widget["key"]))
        continue

    action = random.choice(chosen_widget["actions"])

    value = None

    if action == 'set':
        value = aide.get_concrete_value(chosen_widget['label'])
        pass

    logger.Info(context, _klass, "Main", "Performing action {} on widget {}.".format(action, chosen_widget["key"]))

    ok = rc.perform_action(context, chosen_widget["selector"], action, value)

    if not ok:
        logger.Error(context, _klass, "Main", "Unable to perform action.")
        continue
