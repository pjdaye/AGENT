from aist_common.grammar.component.component import Component
from aist_common.grammar.element_class.dropdown import Dropdown
from aist_common.grammar.element_class.error_message import ErrorMessage
from aist_common.grammar.element_class.Textbox import Textbox
from aist_common.grammar.observation import Observation
from aist_common.grammar.qualifier_classifier import QualifierClassifier


class StateObserver:
    def __init__(self):
        self.qualifier_classifier = QualifierClassifier()
        pass

    def perceive(self, act_state, page_analysis):
        observations = []

        label_candidates = page_analysis['analysis']['labelCandidates']
        error_messages = page_analysis['analysis']['errorMessages']

        for widget in act_state.widgets:
            widget_label = widget['label']
            widget_label_key = widget['label_key']

            if not widget_label:
                continue

            if widget_label_key and widget_label_key not in label_candidates:
                continue

            widget_element_class = self.get_element_class(widget, error_messages)

            if not widget_element_class:
                continue

            widget_ident = widget_label.replace(' ', '').upper()

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
        widget_tag = widget['properties']['tagName']
        if widget_tag == 'INPUT':
            return Textbox()
        elif widget_tag == 'SELECT':
            return Dropdown()
        elif widget['key'] in error_messages:
            return ErrorMessage()
        return None




