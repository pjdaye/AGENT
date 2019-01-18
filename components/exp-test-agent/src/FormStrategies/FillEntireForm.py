

class FillEntireForm:
    def __init__(self, logger, aide):
        self.logger = logger
        self.aide = aide
        self._klass = __class__.__name__

    def execute(self, context, runner, aut_state):
        for actionable_widget in aut_state.widgets:
            if 'set' in actionable_widget['actions']:
                value = self.aide.get_concrete_value(actionable_widget['label'])

                self.logger.Info(context, self._klass, "execute",
                                 "Filling form field {}: {}.".format(actionable_widget['key'], value))

                ok = runner.perform_action(context, actionable_widget["selector"], 'set', value)

                if not ok:
                    self.logger.Error(context, self._klass, "execute",
                                      "Unable to fill form field: " + actionable_widget['key'])
                    return False
        return True

