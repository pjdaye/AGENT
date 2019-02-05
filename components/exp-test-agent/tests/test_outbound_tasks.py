from unittest.mock import patch, Mock

from outbound_tasks import PlannedFlowPublisher


@patch('outbound_tasks.jsonpickle')
@patch('outbound_tasks.coordinator_handle_planned_flow')
def test_publish(coordinator_handle_planned_flow_mock, jsonpickle_mock):
    # Arrange
    concrete_flow = Mock()
    json_out = Mock()
    jsonpickle_mock.encode.return_value = json_out

    # Act
    PlannedFlowPublisher.publish(concrete_flow)

    # Assert
    assert concrete_flow.calculate_hash.called is True
    jsonpickle_mock.encode.assert_called_with(concrete_flow)
    coordinator_handle_planned_flow_mock.delay.assert_called_with(json_out)
