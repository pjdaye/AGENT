from aist_common.log import get_logger

LOGGER = get_logger('fill-entire-form-strategy')


class FillEntireForm:
    def __init__(self, aide):
        self.aide = aide
        self._klass = __class__.__name__

    def execute(self, runner, aut_state):

        actionable_widgets = [w for w in aut_state.widgets if 'set' in w['actions']]
        actionable_widgets = self.aide.get_concrete_values(actionable_widgets)

        for actionable_widget in actionable_widgets:
            LOGGER.info("Filling form field {}: {}.".format(actionable_widget['key'], actionable_widget['value']))

            ok = runner.perform_action(actionable_widget["selector"], 'set', actionable_widget['value'])

            if not ok:
                LOGGER.error(self._klass, "execute", "Unable to fill form field: " + actionable_widget['key'])
                return False
        return True
