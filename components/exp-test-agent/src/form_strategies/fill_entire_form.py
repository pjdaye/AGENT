"""A form filling strategy that attempts to fill out all settable form fields with valid values."""

from aist_common.log import get_logger

LOGGER = get_logger('fill-entire-form-strategy')


class FillEntireForm:
    """A form filling strategy that attempts to fill out all settable form fields with valid values."""

    def __init__(self, form_expert):
        """ Initializes the FillEntireForm class.
        :param form_expert: An instance of the form expert client.
        """

        self.form_expert = form_expert
        self._klass = __class__.__name__

    def execute(self, runner, abstract_state):
        """ Executes the form filling strategy against a given abstract state.

        :param runner: An instance of the runner client (that holds an active runner session).
        :param abstract_state: The current abstract state for the page that needs to be filled out.

        :return: True if all settable form fields were successfully filled.
        """

        actionable_widgets = [w for w in abstract_state.widgets if 'set' in w['actions']]
        actionable_widgets = self.form_expert.get_concrete_values(actionable_widgets)

        for actionable_widget in actionable_widgets:
            LOGGER.debug("Filling form field {}: {}.".format(actionable_widget['key'], actionable_widget['value']))

            ok = runner.perform_action(actionable_widget["selector"], 'set', actionable_widget['value'])

            if not ok:
                LOGGER.error("Unable to fill form field: %s", actionable_widget['key'])
                return False
        return True
