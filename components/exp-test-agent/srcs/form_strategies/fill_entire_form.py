from aist_common.log import get_logger

LOGGER = get_logger('fill-entire-form-strategy')


class FillEntireForm:
    def __init__(self, aide):
        self.aide = aide
        self._klass = __class__.__name__

    def execute(self, runner, aut_state):
        for actionable_widget in aut_state.widgets:
            if 'set' in actionable_widget['actions']:
                value = self.aide.get_concrete_value(actionable_widget['label'])

                LOGGER.info("Filling form field {}: {}.".format(actionable_widget['key'], value))

                ok = runner.perform_action(actionable_widget["selector"], 'set', value)

                if not ok:
                    LOGGER.error(self._klass, "execute", "Unable to fill form field: " + actionable_widget['key'])
                    return False
        return True
