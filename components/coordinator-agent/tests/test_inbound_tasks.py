from unittest.mock import patch, Mock

import inbound_tasks
from inbound_tasks import coordinator_handle_planned_flow


@patch('inbound_tasks.processed_tests', ['planned_flow_mock_hash'])
@patch('inbound_tasks.jsonpickle')
@patch('inbound_tasks.LOGGER')
def test_coordinator_handle_planned_flow_with_planned_hash_in_processed_tests(logger_mock,
                                                                              jsonpickle_mock
):
    # Arrange
    flow_data = Mock()
    planned_flow_mock = Mock()
    planned_flow_mock.hash = 'planned_flow_mock_hash'
    planned_flow_mock.original_flow = 'planned_flow_mock_original_flow'
    jsonpickle_mock.decode.return_value = planned_flow_mock

    # Act
    result = coordinator_handle_planned_flow(flow_data)

    # Assert
    jsonpickle_mock.decode.assert_called_with(flow_data)
    logger_mock.debug.assert_called_with('Received abstract test on COORDINATOR QUEUE: '
                                         '(planned_flow_mock_hash) planned_flow_mock_original_flow. (DUPLICATE)')
    assert result is True


@patch('inbound_tasks.AgentFlowPublisher')
@patch('inbound_tasks.processed_tests', {''})
@patch('inbound_tasks.jsonpickle')
@patch('inbound_tasks.LOGGER')
def test_coordinator_handle_planned_flow_with_planned_hash_in_processed_tests(logger_mock,
                                                                              jsonpickle_mock,
                                                                              agent_flow_publisher_mock
):
    # Arrange
    flow_data = Mock()
    planned_flow_mock = Mock()
    planned_flow_mock.hash = 'planned_flow_mock_hash'
    planned_flow_mock.original_flow = 'planned_flow_mock_original_flow'
    jsonpickle_mock.decode.return_value = planned_flow_mock

    # Act
    result = coordinator_handle_planned_flow(flow_data)

    # Assert
    jsonpickle_mock.decode.assert_called_with(flow_data)
    logger_mock.debug.assert_called_with('Received abstract test on COORDINATOR QUEUE: '
                                         '(planned_flow_mock_hash) planned_flow_mock_original_flow. (NEW)')
    logger_mock.info.assert_called_with('Received abstract test. Publishing to round-robin WORKER QUEUE.')
    agent_flow_publisher_mock.publish.assert_called_with(flow_data)
    assert '' in  inbound_tasks.processed_tests
    assert 'planned_flow_mock_hash' in inbound_tasks.processed_tests
    assert result is True
