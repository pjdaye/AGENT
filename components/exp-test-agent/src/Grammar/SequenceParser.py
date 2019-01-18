from lark import Lark, Transformer

from Grammar.Capture import Capture
from Grammar.Component.Component import Component
from Grammar.Component.ComponentAction import ComponentAction
from Grammar.Component.ComponentActionList import ComponentActionList
from Grammar.Component.ComponentActionUsingCaptured import ComponentActionUsingCaptured
from Grammar.Component.ComponentActionWithCapture import ComponentActionWithCapture
from Grammar.Component.ComponentFocusAction import ComponentFocusAction
from Grammar.ConditionalObservationList import ConditionalObservationList
from Grammar.ElementClass.Cancel import Cancel
from Grammar.ElementClass.Commit import Commit
from Grammar.ElementClass.Dropdown import Dropdown
from Grammar.ElementClass.ErrorMessage import ErrorMessage
from Grammar.ElementClass.LearnedElement import LearnedElement
from Grammar.ElementClass.Textbox import Textbox
from Grammar.EquivalenceClass.Blank import Blank
from Grammar.EquivalenceClass.Invalid import Invalid
from Grammar.EquivalenceClass.InvalidLong import InvalidLong
from Grammar.EquivalenceClass.InvalidSpecialCharacters import InvalidSpecialCharacters
from Grammar.EquivalenceClass.InvalidXsr import InvalidXsr
from Grammar.EquivalenceClass.LearnedEquivalence import LearnedEquivalence
from Grammar.EquivalenceClass.Valid import Valid
from Grammar.EquivalenceClass.Whitespace import Whitespace
from Grammar.NotCapture import NotCapture
from Grammar.Observation import Observation
from Grammar.ObservationInCollection import ObservationInCollection
from Grammar.ObservationList import ObservationList
from Grammar.ObservationWithCapture import ObservationWithCapture
from Grammar.Qualifier.DisabledQualifier import DisabledQualifier
from Grammar.Qualifier.LearnedQualifier import LearnedQualifier
from Grammar.Qualifier.QualifierList import QualifierList
from Grammar.Qualifier.RequiredQualifier import RequiredQualifier
from Grammar.Qualifier.ScreenQualifier import ScreenQualifier
from Grammar.TestFlow import TestFlow


class SequenceParser:
    def __init__(self, grammar_file='Grammar/seq.g'):
        self.parser = Lark(open(grammar_file))

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
