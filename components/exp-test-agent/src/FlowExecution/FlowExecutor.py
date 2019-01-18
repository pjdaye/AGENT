from FormStrategies.FillEntireForm import FillEntireForm


class FlowExecutor:
    def __init__(self, logger, aide, pac, mapper, ext_labels, observer, defect_rep):
        self.log = logger
        self.aide = aide
        self.pac = pac
        self.mapper = mapper
        self.ext_labels = ext_labels
        self.observer = observer
        self.defect_rep = defect_rep
        self.form_fill_strategy = FillEntireForm(logger, aide)
        self._klass = __class__.__name__

    def execute(self, context, initial_state, runner, planned_flow):

        ok = self.form_fill_strategy.execute(context, runner, initial_state)

        if not ok:
            self.log.Error(context, self._klass, "execute", "Unable to execute form fill strategy on state: " + str(initial_state.hash))
            return False

        for step in planned_flow.bound_actions:
            action = step[0]
            widget = step[1]

            if action.action == 'TRY':
                value = self.aide.get_concrete_inputs(action.component.ident, action.equivalence_class.equivalence_class)
                ok = runner.perform_action(context, widget["selector"], "set", value)

                if not ok:
                    self.log.Error(context, self._klass, "execute", "Unable to execute flow act step: " + str(action))
                    return False

                self.log.Info(context, self._klass, "execute", "Successfully executed flow act step: " + str(action))

            elif action.action == 'CLICK':
                ok = runner.perform_action(context, widget["selector"], "click", None)

                if not ok:
                    self.log.Error(context, self._klass, "execute", "Unable to execute flow act step: " + str(action))
                    return False

                self.log.Info(context, self._klass, "execute", "Successfully executed flow act step: " + str(action))

        concrete_state = runner.concrete_state(context)

        if concrete_state is False:
            self.log.Error(context, self._klass, "execute", "Unable to execute flow observe step.")
            return False

        page_analysis = self.pac.run_analysis(context, concrete_state)

        act_state = self.mapper.process(context, concrete_state)

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
                self.log.Info(context, self._klass, "execute", "Found defect on state: " + str(act_state.hash))
                self.defect_rep.add_defect(flow, planned_flow.bound_actions, i)

        return True
