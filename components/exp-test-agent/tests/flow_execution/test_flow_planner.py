from abstraction.actionable_state import ActionableState
from aist_common.grammar.sequence_parser import SequenceParser
from flow_execution.flow_planner import FlowPlanner


def test_happy_path():
    # Arrange.
    to_parse = "OBSERVE TEXTBOX EMAIL TRY VALID EMAIL CLICK COMMIT NOTOBSERVE ERRORMESSAGE"
    parser = SequenceParser()
    abstract_flow = parser.parse(to_parse)

    flow_planner = FlowPlanner()

    page_analysis = {
        'analysis': {
            'COMMIT': ['C1'],
            'ERRORMESSAGE': ['E1']
        }
    }

    abstract_state = ActionableState()

    widget_email = {
        'key': 'EMAIL',
        'label': 'Email',
        'actions': ['set']
    }

    widget_save = {
        'key': 'C1',
        'label': 'Save',
        'actions': ['click']
    }

    widget_error = {
        'key': 'E1',
        'label': 'Error'
    }

    abstract_state.add_widget(widget_email)
    abstract_state.add_widget(widget_save)
    abstract_state.add_widget(widget_error)

    # Act.
    planned = flow_planner.plan(abstract_state, page_analysis, abstract_flow)

    # Assert.
    assert planned is not None
    assert len(planned) == 1

    planned = planned[0]

    assert planned.original_flow is abstract_flow
    assert planned.initial_state is abstract_state

    assert planned.bound_actions is not None
    assert len(planned.bound_actions) == 2

    assert planned.bound_actions[0][0].action == 'TRY'
    assert planned.bound_actions[0][0].component.element_class is None
    assert planned.bound_actions[0][0].component.ident == 'EMAIL'
    assert planned.bound_actions[0][0].equivalence_class.equivalence_class == 'VALID'

    assert planned.bound_actions[0][1] == widget_email

    assert planned.bound_actions[1][0].action == 'CLICK'
    assert planned.bound_actions[1][0].component is None
    assert planned.bound_actions[1][0].equivalence_class.element_class is None
    assert planned.bound_actions[1][0].equivalence_class.ident == 'COMMIT'

    assert planned.bound_actions[1][1] == widget_save


def test_flow_act_step_not_bound_missing_widget():
    # Arrange.
    to_parse = "OBSERVE TEXTBOX EMAIL TRY VALID EMAIL CLICK COMMIT NOTOBSERVE ERRORMESSAGE"
    parser = SequenceParser()
    abstract_flow = parser.parse(to_parse)

    flow_planner = FlowPlanner()

    page_analysis = {
        'analysis': {
            'COMMIT': ['C1'],
            'ERRORMESSAGE': ['E1']
        }
    }

    abstract_state = ActionableState()

    widget_save = {
        'key': 'C1',
        'label': 'Save',
        'actions': ['click']
    }

    widget_error = {
        'key': 'E1',
        'label': 'Error'
    }

    abstract_state.add_widget(widget_save)
    abstract_state.add_widget(widget_error)

    # Act.
    planned = flow_planner.plan(abstract_state, page_analysis, abstract_flow)

    # Assert.
    assert planned is False


def test_flow_act_step_not_bound_missing_class():
    # Arrange.
    to_parse = "OBSERVE TEXTBOX EMAIL TRY VALID EMAIL CLICK COMMIT NOTOBSERVE ERRORMESSAGE"
    parser = SequenceParser()
    abstract_flow = parser.parse(to_parse)

    flow_planner = FlowPlanner()

    page_analysis = {
        'analysis': {
            'ERRORMESSAGE': ['E1']
        }
    }

    abstract_state = ActionableState()

    widget_email = {
        'key': 'EMAIL',
        'label': 'Email',
        'actions': ['set']
    }

    widget_save = {
        'key': 'C1',
        'label': 'Save',
        'actions': ['click']
    }

    widget_error = {
        'key': 'E1',
        'label': 'Error'
    }

    abstract_state.add_widget(widget_email)
    abstract_state.add_widget(widget_save)
    abstract_state.add_widget(widget_error)

    # Act.
    planned = flow_planner.plan(abstract_state, page_analysis, abstract_flow)

    # Assert.
    assert planned is False


def test_flow_act_step_not_bound_missing_classification():
    # Arrange.
    to_parse = "OBSERVE TEXTBOX EMAIL TRY VALID EMAIL CLICK COMMIT NOTOBSERVE ERRORMESSAGE"
    parser = SequenceParser()
    abstract_flow = parser.parse(to_parse)

    flow_planner = FlowPlanner()

    page_analysis = {
        'analysis': {
            'COMMIT': ['X'],
            'ERRORMESSAGE': ['E1']
        }
    }

    abstract_state = ActionableState()

    widget_email = {
        'key': 'EMAIL',
        'label': 'Email',
        'actions': ['set']
    }

    widget_save = {
        'key': 'C1',
        'label': 'Save',
        'actions': ['click']
    }

    widget_error = {
        'key': 'E1',
        'label': 'Error'
    }

    abstract_state.add_widget(widget_email)
    abstract_state.add_widget(widget_save)
    abstract_state.add_widget(widget_error)

    # Act.
    planned = flow_planner.plan(abstract_state, page_analysis, abstract_flow)

    # Assert.
    assert planned == []


def test_flow_act_step_not_bound_missing_widget_action():
    # Arrange.
    to_parse = "OBSERVE TEXTBOX EMAIL TRY VALID EMAIL CLICK COMMIT NOTOBSERVE ERRORMESSAGE"
    parser = SequenceParser()
    abstract_flow = parser.parse(to_parse)

    flow_planner = FlowPlanner()

    page_analysis = {
        'analysis': {
            'COMMIT': ['C1'],
            'ERRORMESSAGE': ['E1']
        }
    }

    abstract_state = ActionableState()

    widget_email = {
        'key': 'EMAIL',
        'label': 'Email',
        'actions': []
    }

    widget_save = {
        'key': 'C1',
        'label': 'Save',
        'actions': ['click']
    }

    widget_error = {
        'key': 'E1',
        'label': 'Error'
    }

    abstract_state.add_widget(widget_email)
    abstract_state.add_widget(widget_save)
    abstract_state.add_widget(widget_error)

    # Act.
    planned = flow_planner.plan(abstract_state, page_analysis, abstract_flow)

    # Assert.
    assert planned is False


def test_flow_act_step_not_bound_missing_commit_action():
    # Arrange.
    to_parse = "OBSERVE TEXTBOX EMAIL TRY VALID EMAIL CLICK COMMIT NOTOBSERVE ERRORMESSAGE"
    parser = SequenceParser()
    abstract_flow = parser.parse(to_parse)

    flow_planner = FlowPlanner()

    page_analysis = {
        'analysis': {
            'COMMIT': ['C1'],
            'ERRORMESSAGE': ['E1']
        }
    }

    abstract_state = ActionableState()

    widget_email = {
        'key': 'EMAIL',
        'label': 'Email',
        'actions': ['set']
    }

    widget_save = {
        'key': 'C1',
        'label': 'Save',
        'actions': []
    }

    widget_error = {
        'key': 'E1',
        'label': 'Error'
    }

    abstract_state.add_widget(widget_email)
    abstract_state.add_widget(widget_save)
    abstract_state.add_widget(widget_error)

    # Act.
    planned = flow_planner.plan(abstract_state, page_analysis, abstract_flow)

    # Assert.
    assert planned == []


def test_multiple_click_candidates():
    # Arrange.
    to_parse = "OBSERVE TEXTBOX EMAIL TRY VALID EMAIL CLICK COMMIT NOTOBSERVE ERRORMESSAGE"
    parser = SequenceParser()
    abstract_flow = parser.parse(to_parse)

    flow_planner = FlowPlanner()

    page_analysis = {
        'analysis': {
            'COMMIT': ['C1', 'C2'],
            'ERRORMESSAGE': ['E1']
        }
    }

    abstract_state = ActionableState()

    widget_email = {
        'key': 'EMAIL',
        'label': 'Email',
        'actions': ['set']
    }

    widget_save = {
        'key': 'C1',
        'label': 'Save',
        'actions': ['click']
    }

    widget_save_2 = {
        'key': 'C2',
        'label': 'Save',
        'actions': ['click']
    }

    widget_error = {
        'key': 'E1',
        'label': 'Error'
    }

    abstract_state.add_widget(widget_email)
    abstract_state.add_widget(widget_save)
    abstract_state.add_widget(widget_save_2)
    abstract_state.add_widget(widget_error)

    # Act.
    planned = flow_planner.plan(abstract_state, page_analysis, abstract_flow)

    # Assert.
    assert planned is not None
    assert len(planned) == 2

    planned_flow = planned[0]

    assert planned_flow.original_flow is abstract_flow
    assert planned_flow.initial_state is abstract_state

    assert planned_flow.bound_actions is not None
    assert len(planned_flow.bound_actions) == 2

    assert planned_flow.bound_actions[0][0].action == 'TRY'
    assert planned_flow.bound_actions[0][0].component.element_class is None
    assert planned_flow.bound_actions[0][0].component.ident == 'EMAIL'
    assert planned_flow.bound_actions[0][0].equivalence_class.equivalence_class == 'VALID'

    assert planned_flow.bound_actions[0][1] == widget_email

    assert planned_flow.bound_actions[1][0].action == 'CLICK'
    assert planned_flow.bound_actions[1][0].component is None
    assert planned_flow.bound_actions[1][0].equivalence_class.element_class is None
    assert planned_flow.bound_actions[1][0].equivalence_class.ident == 'COMMIT'

    assert planned_flow.bound_actions[1][1] == widget_save

    planned_flow = planned[1]

    assert planned_flow.original_flow is abstract_flow
    assert planned_flow.initial_state is abstract_state

    assert planned_flow.bound_actions is not None
    assert len(planned_flow.bound_actions) == 2

    assert planned_flow.bound_actions[0][0].action == 'TRY'
    assert planned_flow.bound_actions[0][0].component.element_class is None
    assert planned_flow.bound_actions[0][0].component.ident == 'EMAIL'
    assert planned_flow.bound_actions[0][0].equivalence_class.equivalence_class == 'VALID'

    assert planned_flow.bound_actions[0][1] == widget_email

    assert planned_flow.bound_actions[1][0].action == 'CLICK'
    assert planned_flow.bound_actions[1][0].component is None
    assert planned_flow.bound_actions[1][0].equivalence_class.element_class is None
    assert planned_flow.bound_actions[1][0].equivalence_class.ident == 'COMMIT'

    assert planned_flow.bound_actions[1][1] == widget_save_2
