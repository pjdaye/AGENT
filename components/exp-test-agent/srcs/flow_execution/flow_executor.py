from form_strategies.fill_entire_form import FillEntireForm

from aist_common.log import get_logger

LOGGER = get_logger('flow-executor')


class FlowExecutor:
    def __init__(self, aide, pac, mapper, ext_labels, observer, defect_rep):
        self.aide = aide
        self.web_classifier = pac
        self.page_abstraction = mapper
        self.ext_labels = ext_labels
        self.observer = observer
        self.defect_rep = defect_rep
        self.form_fill_strategy = FillEntireForm(aide)
        self._klass = __class__.__name__

    def execute(self, initial_state, runner, planned_flow):

        ok = self.form_fill_strategy.execute(runner, initial_state)

        if not ok:
            LOGGER.error("Unable to execute form fill strategy on state: " + str(initial_state.hash))
            return False

        for step in planned_flow.bound_actions:
            action = step[0]
            widget = step[1]

            if action.action == 'TRY':
                value = self.aide.get_concrete_inputs(action.component.ident,
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

        page_analysis = self.web_classifier.run_analysis(concrete_state)

        act_state = self.page_abstraction.process(concrete_state)

        self.ext_labels.extract_labels(act_state, page_analysis)

        observations = self.observer.perceive(act_state, page_analysis)

        actual_observation_hashes = [hash(obs) for obs in observations]

        flow = planned_flow.original_flow

        for i in range(len(flow.observe.observations)):
            expected_observation = flow.observe.observations[i]
            expected_hash = hash(expected_observation)
            success = expected_observation.observe and expected_hash in actual_observation_hashes
            success = success or not expected_observation.observe and expected_hash not in actual_observation_hashes
            if not success:
                LOGGER.info("Found defect on state: " + str(act_state.hash))
                self.defect_rep.add_defect(flow, planned_flow.bound_actions, i)

        return True
