from unittest.mock import patch, Mock

from abstraction.actionable_state import ActionableState
from aist_common.grammar.test_flow import TestFlow

from flow_execution.concrete_test_flow import ConcreteTestFlow


@patch(ConcreteTestFlow.__module__ + '.hash')
@patch(ConcreteTestFlow.__module__ + '.frozenset')
def test_calculate_hash(frozenset_mock, hash_mock):
    # Arrange
    abstract_state = ActionableState()
    abstract_state.hash = 'abstract_state_hash'
    bound_actions = [
        ['bound_action_1', {'key': 'key_1'}],
        ['bound_action_2', {'key': 'key_2'}]
    ]

    perceive, act, observe = Mock(), Mock(), Mock()

    observe.observe = Mock()
    observe.observations = ['observe_step_1', 'observe_step_2']

    original_flow = TestFlow(perceive, act, observe)

    concrete_test_flow = ConcreteTestFlow(
        'path',
        abstract_state,
        original_flow,
        bound_actions)

    frozenset_mock_return_value = Mock()
    frozenset_mock.return_value = frozenset_mock_return_value
    hash_mock_return_value = Mock()
    hash_mock.return_value = hash_mock_return_value

    # Act
    concrete_test_flow.calculate_hash()

    # Assert
    assert concrete_test_flow.hash == hash_mock_return_value
    frozenset_mock.assert_called_with(
        (
            'abstract_state_hash',
            'bound_action_1',
            'key_1',
            'bound_action_2',
            'key_2',
            'observe_step_1',
            'observe_step_2'
        )
    )
    hash_mock.assert_called_with(frozenset_mock_return_value)
