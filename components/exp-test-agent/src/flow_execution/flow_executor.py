"""Executes a concrete test flow."""
from form_strategies.fill_entire_form import FillEntireForm

from aist_common.log import get_logger

LOGGER = get_logger('flow-executor')


class FlowExecutor:
    """Executes a concrete test flow."""

    def __init__(self, form_expert, page_analyzer, state_abstracter, label_extracter, observer, defect_rep):
        """ Initializes the FlowExecutor class.
        
        :param form_expert: An instance of the form expert client.
        :param page_analyzer: An instance of the page analyzer client.
        :param state_abstracter: An instance of the StateAbstracter class.
        :param label_extracter: An instance of the LabelExtraction class.
        :param observer: An instance of the StateObserver class.
        :param defect_rep: An instance of the DefectReporter class.
        """

        self.form_expert = form_expert
        self.page_analyzer = page_analyzer
        self.state_abstracter = state_abstracter
        self.ext_labels = label_extracter
        self.observer = observer
        self.defect_rep = defect_rep
        self.form_fill_strategy = FillEntireForm(form_expert)
        self._klass = __class__.__name__

    def execute(self, initial_state, runner, concrete_flow):
        """ Executes a concrete test flow. Reports any issues found during execution.

        :param initial_state: The current abstract state (where the concrete test flow execution begins from).
        :param runner: An instance of the runner client (that holds an active runner session).
        :param concrete_flow: The concrete test flow to execute.

        :return: True if the concrete test flow execution succeeded.
        """

        ok = self.form_fill_strategy.execute(runner, initial_state)

        if not ok:
            LOGGER.error("Unable to execute form fill strategy on state: " + str(initial_state.hash))
            return False

        for step in concrete_flow.bound_actions:
            action = step[0]
            widget = step[1]

            if action.action == 'TRY':
                value = self.form_expert.get_concrete_inputs(action.component.ident,
                                                      action.equivalence_class.equivalence_class)

                ok = runner.perform_action(widget["selector"], "set", value)

                if not ok:
                    LOGGER.error("Unable to execute flow act step: " + str(action))
                    return False

                LOGGER.info("Successfully executed flow act step: " + str(action))

            elif action.action == 'CLICK':
                ok = runner.perform_action(widget["selector"], "click", None)

                if not ok:
                    LOGGER.error("Unable to execute flow act step: " + str(action))
                    return False

                LOGGER.info("Successfully executed flow act step: " + str(action))

        concrete_state = runner.concrete_state()

        if concrete_state is False:
            LOGGER.error("Unable to execute flow observe step.")
            return False

        page_analysis = self.page_analyzer.run_analysis(concrete_state)

        act_state = self.state_abstracter.process(concrete_state)

        self.ext_labels.extract_labels(act_state, page_analysis)

        observations = self.observer.perceive(act_state, page_analysis)

        actual_observation_hashes = [hash(obs) for obs in observations]

        flow = concrete_flow.original_flow

        for i in range(len(flow.observe.observations)):
            expected_observation = flow.observe.observations[i]
            expected_hash = hash(expected_observation)
            success = expected_observation.observe and expected_hash in actual_observation_hashes
            success = success or not expected_observation.observe and expected_hash not in actual_observation_hashes
            if not success:
                LOGGER.info("Found defect on state: " + str(act_state.hash))
                self.defect_rep.add_defect(flow, concrete_flow.bound_actions, i)

        return True
