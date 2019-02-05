from unittest.mock import patch, Mock

from flow_execution.concrete_test_flow import ConcreteTestFlow


@patch('ConcreteTestFlow.hash')
@patch('ConcreteTestFlow.frozenset')
def test_calculate_hash(frozenset_mock, hash_mock):
    # Arrange
    abstract_state = ()
    abstract_state.hash = 'abstract_state_hash'
    bound_actions = [
        ['bound_action_1', {'key': 'key_1'}],
        ['bound_action_2', {'key': 'key_2'}]
    ]
    original_flow = ()
    original_flow.observe = ()
    original_flow.observations = ['observe_step_1', 'observe_step_2']
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
    hash = concrete_test_flow.calculate_hash()

    # Assert
    assert hash == hash_mock_return_value
    frozenset_mock.assert_called_with('test')
    hash_mock.assert_called_with(frozenset_mock_return_value)
