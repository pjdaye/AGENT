"""Responsible for extracting observations from an abstract state."""

from aist_common.grammar.component.component import Component
from aist_common.grammar.element_class.dropdown import Dropdown
from aist_common.grammar.element_class.error_message import ErrorMessage
from aist_common.grammar.element_class.Textbox import Textbox
from aist_common.grammar.observation import Observation
from aist_common.grammar.qualifier_classifier import QualifierClassifier


class StateObserver:
    """Responsible for extracting observations from an abstract state."""

    def __init__(self):
        """ Initializes the StateObserver class.
        """

        self.qualifier_classifier = QualifierClassifier()

    def perceive(self, abstract_state, page_analysis):
        """ Extracts observations from a given abstract state in the form of grammar ASTs.
            Relies on element classifications present in the provided page analysis to qualify elements.

        :param abstract_state: The abstract state to process.
        :param page_analysis: The page analysis output for the provided abstract state (element classifications).

        :return: A list of observations, each an instance of our grammar's Observation class.
        """

        observations = []

        label_candidates = page_analysis['analysis']['labelCandidates']
        error_messages = page_analysis['analysis']['errorMessages']

        for widget in abstract_state.get_all_widgets():
            widget_label = widget['label'] if 'label' in widget else None
            widget_label_key = widget['label_key'] if 'label_key' in widget else None

            if not widget_label:
                continue

            if widget_label_key and widget_label_key not in label_candidates:
                continue

            widget_element_class = self.get_element_class(widget, error_messages)

            if not widget_element_class:
                continue

            widget_ident = widget_label.replace(' ', '').upper()

            if isinstance(widget_element_class, ErrorMessage):
                widget_component = Component(widget_element_class, None)
            else:
                widget_component = Component(widget_element_class, widget_ident)

            widget_observation = Observation().positive().with_component(widget_component)

            # TODO: Handle qualifiers.
            # qualifiers = self.qualifier_classifier.get_qualifiers(act_state)
            # widget_key = widget['key']
            # if widget_key in qualifiers:
            #     for qualifier in qualifiers:
            #         pass

            observations.append(widget_observation)

        return observations

    @staticmethod
    def get_element_class(widget, error_messages):
        """ Maps a widget to an element class (e.g. Textbox, Dropdown, ErrorMessage).

        :param widget: The abstract widget to map.
        :param error_messages: The list of error messages present on the abstract state being processed.
        :return: The element class for the provided widget.
        """

        widget_tag = widget['properties']['tagName']
        if widget_tag == 'INPUT':
            return Textbox()
        elif widget_tag == 'SELECT':
            return Dropdown()
        elif widget['key'] in error_messages:
            return ErrorMessage()
        return None
