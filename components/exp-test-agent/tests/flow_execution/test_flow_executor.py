from unittest.mock import Mock

from abstraction.actionable_state import ActionableState
from abstraction.state_abstracter import StateAbstracter
from aist_common.grammar.sequence_parser import SequenceParser
from flow_execution.flow_executor import FlowExecutor
from flow_execution.flow_planner import FlowPlanner
from perceive.label_extraction import LabelExtraction
from perceive.state_observer import StateObserver


def test_happy_path():
    # Arrange.
    form_expert = Mock()
    page_analyzer = Mock()
    state_abstracter = StateAbstracter()
    label_extracter = LabelExtraction()
    observer = StateObserver()
    defect_rep = Mock()

    flow_executor = FlowExecutor(form_expert, page_analyzer, state_abstracter, label_extracter, observer, defect_rep)
    flow_executor.form_fill_strategy = Mock()

    to_parse = "OBSERVE TEXTBOX EMAIL TRY VALID EMAIL CLICK COMMIT OBSERVE ERRORMESSAGE"
    parser = SequenceParser()
    abstract_flow = parser.parse(to_parse)

    flow_planner = FlowPlanner()

    page_analysis = {
        'analysis': {
            'labelCandidates': ['Label_Email'],
            'COMMIT': ['C1'],
            'ERRORMESSAGE': ['E1'],
            'errorMessages': ['E1']
        }
    }

    page_analyzer.run_analysis.return_value = page_analysis

    abstract_state = ActionableState()

    widget_email_label = {
        'key': 'Label_Email',
        'label': 'EmailLabel',
        'actions': [],
        'selector': '#lblEmail',
        'properties': {
            'tagName': 'LABEL',
            'text': 'E-mail',
            'x': 10,
            'y': 10
        }
    }

    widget_email = {
        'key': 'EMAIL',
        'label': 'Email',
        'actions': ['set'],
        'selector': '#email',
        'properties': {
            'tagName': 'INPUT',
            'x': 20,
            'y': 20
        }
    }

    widget_save = {
        'key': 'C1',
        'label': 'Save',
        'actions': ['click'],
        'selector': '#save',
        'properties': {
            'tagName': 'BUTTON',
            'x': 40,
            'y': 40
        }
    }

    widget_error = {
        'key': 'E1',
        'label': 'Error',
        'properties': {
            'tagName': 'LABEL',
            'x': 60,
            'y': 60
        }
    }

    abstract_state.add_widget(widget_email_label)
    abstract_state.add_widget(widget_email)
    abstract_state.add_widget(widget_save)
    abstract_state.add_widget(widget_error)

    target_concrete_state = {
        'widgets': {
            'Label_Email': widget_email_label,
            'EMAIL': widget_email,
            'C1': widget_save,
            'E1': widget_error
        }
    }

    runner_mock = Mock()
    runner_mock.concrete_state.return_value = target_concrete_state

    planned = flow_planner.plan(abstract_state, page_analysis, abstract_flow)
    planned_flow = planned[0]

    # Act.
    resp = flow_executor.execute(abstract_state, runner_mock, planned_flow)

    # Assert.
    assert resp is True
    assert not defect_rep.add_defect.called


def test_failed_observation_step():
    # Arrange.
    form_expert = Mock()
    page_analyzer = Mock()
    state_abstracter = StateAbstracter()
    label_extracter = LabelExtraction()
    observer = StateObserver()
    defect_rep = Mock()

    flow_executor = FlowExecutor(form_expert, page_analyzer, state_abstracter, label_extracter, observer, defect_rep)
    flow_executor.form_fill_strategy = Mock()

    to_parse = "OBSERVE TEXTBOX EMAIL TRY VALID EMAIL CLICK COMMIT NOTOBSERVE ERRORMESSAGE"
    parser = SequenceParser()
    abstract_flow = parser.parse(to_parse)

    flow_planner = FlowPlanner()

    page_analysis = {
        'analysis': {
            'labelCandidates': ['Label_Email'],
            'COMMIT': ['C1'],
            'ERRORMESSAGE': ['E1'],
            'errorMessages': ['E1']
        }
    }

    page_analyzer.run_analysis.return_value = page_analysis

    abstract_state = ActionableState()

    widget_email_label = {
        'key': 'Label_Email',
        'label': 'EmailLabel',
        'actions': [],
        'selector': '#lblEmail',
        'properties': {
            'tagName': 'LABEL',
            'text': 'E-mail',
            'x': 10,
            'y': 10
        }
    }

    widget_email = {
        'key': 'EMAIL',
        'label': 'Email',
        'actions': ['set'],
        'selector': '#email',
        'properties': {
            'tagName': 'INPUT',
            'x': 20,
            'y': 20
        }
    }

    widget_save = {
        'key': 'C1',
        'label': 'Save',
        'actions': ['click'],
        'selector': '#save',
        'properties': {
            'tagName': 'BUTTON',
            'x': 40,
            'y': 40
        }
    }

    widget_error = {
        'key': 'E1',
        'label': 'Error',
        'properties': {
            'tagName': 'LABEL',
            'x': 60,
            'y': 60
        }
    }

    abstract_state.add_widget(widget_email_label)
    abstract_state.add_widget(widget_email)
    abstract_state.add_widget(widget_save)
    abstract_state.add_widget(widget_error)

    target_concrete_state = {
        'widgets': {
            'Label_Email': widget_email_label,
            'EMAIL': widget_email,
            'C1': widget_save,
            'E1': widget_error
        }
    }

    runner_mock = Mock()
    runner_mock.concrete_state.return_value = target_concrete_state

    planned = flow_planner.plan(abstract_state, page_analysis, abstract_flow)
    planned_flow = planned[0]

    # Act.
    resp = flow_executor.execute(abstract_state, runner_mock, planned_flow)

    # Assert.
    assert resp is True
    assert defect_rep.add_defect.called


def test_unable_to_fill_form():
    # Arrange.
    form_expert = Mock()
    page_analyzer = Mock()
    state_abstracter = StateAbstracter()
    label_extracter = LabelExtraction()
    observer = StateObserver()
    defect_rep = Mock()

    flow_executor = FlowExecutor(form_expert, page_analyzer, state_abstracter, label_extracter, observer, defect_rep)
    flow_executor.form_fill_strategy = Mock()
    flow_executor.form_fill_strategy.execute.return_value = False

    to_parse = "OBSERVE TEXTBOX EMAIL TRY VALID EMAIL CLICK COMMIT NOTOBSERVE ERRORMESSAGE"
    parser = SequenceParser()
    abstract_flow = parser.parse(to_parse)

    flow_planner = FlowPlanner()

    page_analysis = {
        'analysis': {
            'labelCandidates': ['Label_Email'],
            'COMMIT': ['C1'],
            'ERRORMESSAGE': ['E1'],
            'errorMessages': ['E1']
        }
    }

    page_analyzer.run_analysis.return_value = page_analysis

    abstract_state = ActionableState()

    widget_email_label = {
        'key': 'Label_Email',
        'label': 'EmailLabel',
        'actions': [],
        'selector': '#lblEmail',
        'properties': {
            'tagName': 'LABEL',
            'text': 'E-mail',
            'x': 10,
            'y': 10
        }
    }

    widget_email = {
        'key': 'EMAIL',
        'label': 'Email',
        'actions': ['set'],
        'selector': '#email',
        'properties': {
            'tagName': 'INPUT',
            'x': 20,
            'y': 20
        }
    }

    widget_save = {
        'key': 'C1',
        'label': 'Save',
        'actions': ['click'],
        'selector': '#save',
        'properties': {
            'tagName': 'BUTTON',
            'x': 40,
            'y': 40
        }
    }

    widget_error = {
        'key': 'E1',
        'label': 'Error',
        'properties': {
            'tagName': 'LABEL',
            'x': 60,
            'y': 60
        }
    }

    abstract_state.add_widget(widget_email_label)
    abstract_state.add_widget(widget_email)
    abstract_state.add_widget(widget_save)
    abstract_state.add_widget(widget_error)

    target_concrete_state = {
        'widgets': {
            'Label_Email': widget_email_label,
            'EMAIL': widget_email,
            'C1': widget_save,
            'E1': widget_error
        }
    }

    runner_mock = Mock()
    runner_mock.concrete_state.return_value = target_concrete_state

    planned = flow_planner.plan(abstract_state, page_analysis, abstract_flow)
    planned_flow = planned[0]

    # Act.
    resp = flow_executor.execute(abstract_state, runner_mock, planned_flow)

    # Assert.
    assert resp is False


def test_unable_to_perform_runner_action():
    # Arrange.
    form_expert = Mock()
    page_analyzer = Mock()
    state_abstracter = StateAbstracter()
    label_extracter = LabelExtraction()
    observer = StateObserver()
    defect_rep = Mock()

    flow_executor = FlowExecutor(form_expert, page_analyzer, state_abstracter, label_extracter, observer, defect_rep)
    flow_executor.form_fill_strategy = Mock()

    to_parse = "OBSERVE TEXTBOX EMAIL TRY VALID EMAIL CLICK COMMIT NOTOBSERVE ERRORMESSAGE"
    parser = SequenceParser()
    abstract_flow = parser.parse(to_parse)

    flow_planner = FlowPlanner()

    page_analysis = {
        'analysis': {
            'labelCandidates': ['Label_Email'],
            'COMMIT': ['C1'],
            'ERRORMESSAGE': ['E1'],
            'errorMessages': ['E1']
        }
    }

    page_analyzer.run_analysis.return_value = page_analysis

    abstract_state = ActionableState()

    widget_email_label = {
        'key': 'Label_Email',
        'label': 'EmailLabel',
        'actions': [],
        'selector': '#lblEmail',
        'properties': {
            'tagName': 'LABEL',
            'text': 'E-mail',
            'x': 10,
            'y': 10
        }
    }

    widget_email = {
        'key': 'EMAIL',
        'label': 'Email',
        'actions': ['set'],
        'selector': '#email',
        'properties': {
            'tagName': 'INPUT',
            'x': 20,
            'y': 20
        }
    }

    widget_save = {
        'key': 'C1',
        'label': 'Save',
        'actions': ['click'],
        'selector': '#save',
        'properties': {
            'tagName': 'BUTTON',
            'x': 40,
            'y': 40
        }
    }

    widget_error = {
        'key': 'E1',
        'label': 'Error',
        'properties': {
            'tagName': 'LABEL',
            'x': 60,
            'y': 60
        }
    }

    abstract_state.add_widget(widget_email_label)
    abstract_state.add_widget(widget_email)
    abstract_state.add_widget(widget_save)
    abstract_state.add_widget(widget_error)

    target_concrete_state = {
        'widgets': {
            'Label_Email': widget_email_label,
            'EMAIL': widget_email,
            'C1': widget_save,
            'E1': widget_error
        }
    }

    runner_mock = Mock()
    runner_mock.concrete_state.return_value = target_concrete_state
    runner_mock.perform_action.return_value = False

    planned = flow_planner.plan(abstract_state, page_analysis, abstract_flow)
    planned_flow = planned[0]

    # Act.
    resp = flow_executor.execute(abstract_state, runner_mock, planned_flow)

    # Assert.
    assert resp is False


def test_unable_to_perform_concrete_state_scrape():
    # Arrange.
    form_expert = Mock()
    page_analyzer = Mock()
    state_abstracter = StateAbstracter()
    label_extracter = LabelExtraction()
    observer = StateObserver()
    defect_rep = Mock()

    flow_executor = FlowExecutor(form_expert, page_analyzer, state_abstracter, label_extracter, observer, defect_rep)
    flow_executor.form_fill_strategy = Mock()

    to_parse = "OBSERVE TEXTBOX EMAIL TRY VALID EMAIL CLICK COMMIT NOTOBSERVE ERRORMESSAGE"
    parser = SequenceParser()
    abstract_flow = parser.parse(to_parse)

    flow_planner = FlowPlanner()

    page_analysis = {
        'analysis': {
            'labelCandidates': ['Label_Email'],
            'COMMIT': ['C1'],
            'ERRORMESSAGE': ['E1'],
            'errorMessages': ['E1']
        }
    }

    page_analyzer.run_analysis.return_value = page_analysis

    abstract_state = ActionableState()

    widget_email_label = {
        'key': 'Label_Email',
        'label': 'EmailLabel',
        'actions': [],
        'selector': '#lblEmail',
        'properties': {
            'tagName': 'LABEL',
            'text': 'E-mail',
            'x': 10,
            'y': 10
        }
    }

    widget_email = {
        'key': 'EMAIL',
        'label': 'Email',
        'actions': ['set'],
        'selector': '#email',
        'properties': {
            'tagName': 'INPUT',
            'x': 20,
            'y': 20
        }
    }

    widget_save = {
        'key': 'C1',
        'label': 'Save',
        'actions': ['click'],
        'selector': '#save',
        'properties': {
            'tagName': 'BUTTON',
            'x': 40,
            'y': 40
        }
    }

    widget_error = {
        'key': 'E1',
        'label': 'Error',
        'properties': {
            'tagName': 'LABEL',
            'x': 60,
            'y': 60
        }
    }

    abstract_state.add_widget(widget_email_label)
    abstract_state.add_widget(widget_email)
    abstract_state.add_widget(widget_save)
    abstract_state.add_widget(widget_error)

    runner_mock = Mock()
    runner_mock.concrete_state.return_value = False

    planned = flow_planner.plan(abstract_state, page_analysis, abstract_flow)
    planned_flow = planned[0]

    # Act.
    resp = flow_executor.execute(abstract_state, runner_mock, planned_flow)

    # Assert.
    assert resp is False


def test_unable_to_perform_runner_click_action():
    # Arrange.
    form_expert = Mock()
    page_analyzer = Mock()
    state_abstracter = StateAbstracter()
    label_extracter = LabelExtraction()
    observer = StateObserver()
    defect_rep = Mock()

    flow_executor = FlowExecutor(form_expert, page_analyzer, state_abstracter, label_extracter, observer, defect_rep)
    flow_executor.form_fill_strategy = Mock()

    to_parse = "OBSERVE TEXTBOX EMAIL TRY VALID EMAIL CLICK COMMIT NOTOBSERVE ERRORMESSAGE"
    parser = SequenceParser()
    abstract_flow = parser.parse(to_parse)

    flow_planner = FlowPlanner()

    page_analysis = {
        'analysis': {
            'labelCandidates': ['Label_Email'],
            'COMMIT': ['C1'],
            'ERRORMESSAGE': ['E1'],
            'errorMessages': ['E1']
        }
    }

    page_analyzer.run_analysis.return_value = page_analysis

    abstract_state = ActionableState()

    widget_email_label = {
        'key': 'Label_Email',
        'label': 'EmailLabel',
        'actions': [],
        'selector': '#lblEmail',
        'properties': {
            'tagName': 'LABEL',
            'text': 'E-mail',
            'x': 10,
            'y': 10
        }
    }

    widget_email = {
        'key': 'EMAIL',
        'label': 'Email',
        'actions': ['set'],
        'selector': '#email',
        'properties': {
            'tagName': 'INPUT',
            'x': 20,
            'y': 20
        }
    }

    widget_save = {
        'key': 'C1',
        'label': 'Save',
        'actions': ['click'],
        'selector': '#save',
        'properties': {
            'tagName': 'BUTTON',
            'x': 40,
            'y': 40
        }
    }

    widget_error = {
        'key': 'E1',
        'label': 'Error',
        'properties': {
            'tagName': 'LABEL',
            'x': 60,
            'y': 60
        }
    }

    abstract_state.add_widget(widget_email_label)
    abstract_state.add_widget(widget_email)
    abstract_state.add_widget(widget_save)
    abstract_state.add_widget(widget_error)

    target_concrete_state = {
        'widgets': {
            'Label_Email': widget_email_label,
            'EMAIL': widget_email,
            'C1': widget_save,
            'E1': widget_error
        }
    }

    runner_mock = Mock()
    runner_mock.concrete_state.return_value = target_concrete_state

    def click_side_effect(*args, **kwargs):
        if args[1] == 'click':
            return False
        return True

    runner_mock.perform_action.side_effect = click_side_effect

    planned = flow_planner.plan(abstract_state, page_analysis, abstract_flow)
    planned_flow = planned[0]

    # Act.
    resp = flow_executor.execute(abstract_state, runner_mock, planned_flow)

    # Assert.
    assert resp is False
