from unittest.mock import Mock, patch
import pytest
from clients.runner_client import RunnerClient
from abstraction.actionable_state import ActionableState
from form_strategies.fill_entire_form import FillEntireForm


@pytest.fixture
def runner():
    runner_mock = Mock(spec=RunnerClient)
    runner_mock.perform_action.return_value = True
    return runner_mock


@pytest.fixture
def form_expert():

    # noinspection PyMethodMayBeStatic
    class FormExpertStub:
        def get_concrete_values(self, widgets):
            for widget in widgets:
                widget['value'] = 'Guido'
            return widgets

    form_expert_stub = FormExpertStub()

    return form_expert_stub


def test_execute_form_fill_with_no_actionable_widgets_returns_true(runner, form_expert):
    # Arrange
    actionable_state = ActionableState()
    form_fill_strategy = FillEntireForm(form_expert)

    # Act
    result = form_fill_strategy.execute(runner, actionable_state)

    # Assert
    assert result is True


def test_execute_form_fill_with_one_settable_widget_returns_true(runner, form_expert):
    # Arrange
    actionable_state = ActionableState()
    widget = {
        'actions': ['set'],
        'label': 'widget_label',
        'key': 'widget_key',
        'selector': 'widget_selector'
    }
    actionable_state.add_widget(widget)
    form_fill_strategy = FillEntireForm(form_expert)

    # Act
    result = form_fill_strategy.execute(runner, actionable_state)

    # Assert
    assert result is True


def test_execute_form_fill_with_one_settable_widget_calls_runner_perform_action_once(runner, form_expert):
    # Arrange
    actionable_state = ActionableState()
    widget = {
        'actions': ['set'],
        'label': 'widget_label',
        'key': 'widget_key',
        'selector': 'widget_selector'
    }
    actionable_state.add_widget(widget)
    form_fill_strategy = FillEntireForm(form_expert)

    # Act
    form_fill_strategy.execute(runner, actionable_state)

    # Assert
    runner.perform_action.assert_called_once()


def test_execute_form_fill_with_two_settable_widgets_calls_runner_perform_action_twice(runner, form_expert):
    # Arrange
    actionable_state = ActionableState()
    widget = {
        'actions': ['set'],
        'label': 'widget_label',
        'key': 'widget_key',
        'selector': 'widget_selector'
    }
    actionable_state.add_widget(widget)
    actionable_state.add_widget(widget)
    form_fill_strategy = FillEntireForm(form_expert)

    # Act
    form_fill_strategy.execute(runner, actionable_state)

    # Assert
    assert runner.perform_action.call_count == 2


def test_execute_form_fill_with_one_non_settable_widget_does_not_perform_action(runner, form_expert):
    # Arrange
    actionable_state = ActionableState()
    widget = {
        'actions': [],
        'label': 'widget_label',
        'key': 'widget_key',
        'selector': 'widget_selector'
    }
    actionable_state.add_widget(widget)
    form_fill_strategy = FillEntireForm(form_expert)

    # Act
    form_fill_strategy.execute(runner, actionable_state)

    # Assert
    runner.perform_action.assert_not_called()

def test_execute_form_fill_returns_false_when_perform_action_fails(runner, form_expert):
    # Arrange
    actionable_state = ActionableState()
    widget = {
        'actions': ['set'],
        'label': 'widget_label',
        'key': 'widget_key',
        'selector': 'widget_selector'
    }
    actionable_state.add_widget(widget)
    runner.perform_action.return_value = False
    form_fill_strategy = FillEntireForm(form_expert)

    # Act
    result = form_fill_strategy.execute(runner, actionable_state)

    # Assert
    assert result is False


