import pkg_resources
from lark import Lark, Transformer

from aist_common.grammar.capture import Capture
from aist_common.grammar.component.component import Component
from aist_common.grammar.component.component_action import ComponentAction
from aist_common.grammar.component.component_action_list import ComponentActionList
from aist_common.grammar.component.component_action_using_captured import ComponentActionUsingCaptured
from aist_common.grammar.component.component_action_with_capture import ComponentActionWithCapture
from aist_common.grammar.component.component_focus_action import ComponentFocusAction
from aist_common.grammar.conditional_observation_list import ConditionalObservationList
from aist_common.grammar.element_class.cancel import Cancel
from aist_common.grammar.element_class.commit import Commit
from aist_common.grammar.element_class.dropdown import Dropdown
from aist_common.grammar.element_class.error_message import ErrorMessage
from aist_common.grammar.element_class.learned_element import LearnedElement
from aist_common.grammar.element_class.Textbox import Textbox
from aist_common.grammar.equivalence_class.blank import Blank
from aist_common.grammar.equivalence_class.invalid import Invalid
from aist_common.grammar.equivalence_class.invalid_long import InvalidLong
from aist_common.grammar.equivalence_class.invalid_special_characters import InvalidSpecialCharacters
from aist_common.grammar.equivalence_class.invalid_xsr import InvalidXsr
from aist_common.grammar.equivalence_class.learned_equivalence import LearnedEquivalence
from aist_common.grammar.equivalence_class.valid import Valid
from aist_common.grammar.equivalence_class.whitespace import Whitespace
from aist_common.grammar.not_capture import NotCapture
from aist_common.grammar.observation import Observation
from aist_common.grammar.observation_in_collection import ObservationInCollection
from aist_common.grammar.observation_list import ObservationList
from aist_common.grammar.observation_with_capture import ObservationWithCapture
from aist_common.grammar.qualifier.disabled_qualifier import DisabledQualifier
from aist_common.grammar.qualifier.learned_qualifier import LearnedQualifier
from aist_common.grammar.qualifier.qualifier_list import QualifierList
from aist_common.grammar.qualifier.required_qualifier import RequiredQualifier
from aist_common.grammar.qualifier.screen_qualifier import ScreenQualifier
from aist_common.grammar.test_flow import TestFlow


class SequenceParser:
    def __init__(self):
        grammar_data = pkg_resources.resource_filename(__name__, 'seq.g')
        self.parser = Lark(open(grammar_data))

    def parse(self, sequence):
        tree = self.parser.parse(sequence)
        xform = SequenceTransformer().transform(tree)
        return xform


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class SequenceTransformer(Transformer):
    def test_flow(self, val):
        return TestFlow(val[0], val[2], val[4])

    def conditional_observation_list(self, val):
        return val[1]

    def conditional_list_sublist(self, val):
        observation_list = val[3]
        observation_list.insert_observation(val[0])
        return observation_list

    def conditional_list_single(self, val):
        return ConditionalObservationList([val[0]])

    def observation_list_sublist(self, val):
        observation_list = val[2]
        observation_list.insert_observation(val[0])
        return observation_list

    def observation_list_single(self, val):
        return ObservationList([val[0]])

    def observe(self, val):
        obs = Observation().positive()
        if len(val) == 2:
            obs.with_component(val[1])
        elif len(val) == 4:
            obs.qualifier_list = val[1]
            obs.with_component(val[3])
        else:
            obs.qualifier_list = val[1]
            obs.with_component(val[2])
        return obs

    def not_observe(self, val):
        obs = Observation().negative()
        if len(val) == 2:
            obs.with_component(val[1])
        elif len(val) == 4:
            obs.qualifier_list = val[1]
            obs.with_component(val[3])
        else:
            obs.qualifier_list = val[1]
            obs.with_component(val[2])
        return obs

    def observe_in_collection(self, val):
        obs = ObservationInCollection().positive()
        obs.with_capture(val[1])
        return obs

    def not_observe_in_collection(self, val):
        obs = ObservationInCollection().negative()
        obs.with_capture(val[1])
        return obs

    def observe_capture(self, val):
        obs = ObservationWithCapture().positive()
        if len(val) == 2:
            obs.with_component(val[1])
            obs.with_capture(val[3])
        elif len(val) == 4:
            obs.with_component(val[1])
            obs.with_capture(val[3])
        else:
            obs.qualifier_list = val[1]
            obs.with_component(val[2])
            obs.with_capture(val[3])
        return obs

    def qualifier_list_sublist(self, val):
        qualifier_list = val[2]
        qualifier_list.insert_qualifier(val[0])
        return qualifier_list

    def qualifier_list_single(self, val):
        return QualifierList([val[0]])

    def screen(self, val):
        return ScreenQualifier()

    def required(self, val):
        return RequiredQualifier()

    def disabled(self, val):
        return DisabledQualifier()

    def learned_qualifier(self, val):
        qual = str(val[0])
        return LearnedQualifier(qual)

    def component_action_list_sublist(self, val):
        component_list = val[2]
        component_list.insert_action(val[0])
        return component_list

    def component_action_list_single(self, val):
        return ComponentActionList([val[0]])

    def try_(self, val):
        action = "TRY"
        eq_class = val[1]
        component = val[3]
        return ComponentAction(action, eq_class, component)

    def try_capture(self, val):
        action = "TRY"
        eq_class = val[1]
        component = val[3]
        capture = val[5]
        return ComponentActionWithCapture(action, eq_class, component, capture)

    def try_captured(self, val):
        action = "TRY"
        captured = val[1]
        component = val[3]
        return ComponentActionUsingCaptured(captured, component)

    def click(self, val):
        action = "CLICK"
        element_class = val[1]
        if hasattr(element_class, 'children'):
            element_class = element_class.children[0]
        return ComponentAction(action, element_class, None)

    def enter(self, val):
        action = "ENTER"
        element_class = val[1]
        if hasattr(element_class, 'children'):
            element_class = element_class.children[0]
        return ComponentAction(action, element_class, None)

    def navigate(self, val):
        action = "NAVIGATE"
        element_class = val[1]
        if hasattr(element_class, 'children'):
            element_class = element_class.children[0]
        return ComponentAction(action, element_class, None)

    def focus_in_collection(self, val):
        action = "FOCUS"
        capture = val[1]
        return ComponentFocusAction(capture)

    def component_1(self, val):
        element_class = val[0]
        if hasattr(element_class, 'children'):
            element_class = element_class.children[0]
        ident = str(val[2])
        return Component(element_class, ident)

    def component_2(self, val):
        element_class = val[0]
        if hasattr(element_class, 'children'):
            element_class = element_class.children[0]
        return Component(element_class, None)

    def component_3(self, val):
        ident = str(val[0])
        return Component(None, ident)

    def valid(self, val):
        return Valid()

    def invalid(self, val):
        return Invalid()

    def blank(self, val):
        return Blank()

    def whitespace(self, val):
        return Whitespace()

    def invalid_long(self, val):
        return InvalidLong()

    def invalid_special_characters(self, val):
        return InvalidSpecialCharacters()

    def invalid_xsr(self, val):
        return InvalidXsr()

    def learned_eq_class(self, val):
        eq_class = str(val[0])
        return LearnedEquivalence(eq_class)

    def textbox(self, val):
        return Textbox()

    def dropdown(self, val):
        return Dropdown()

    def error_message(self, val):
        return ErrorMessage()

    def commit(self, val):
        return Commit()

    def cancel(self, val):
        return Cancel()

    def learned_el_class(self, val):
        el_class = str(val[0])
        return LearnedElement(el_class)

    def capture(self, val):
        return Capture(str(val[0]))

    def not_capture(self, val):
        return NotCapture(str(val[0]))
