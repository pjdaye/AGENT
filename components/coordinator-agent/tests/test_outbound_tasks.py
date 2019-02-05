from unittest.mock import patch, Mock

from outbound_tasks import AgentFlowPublisher


@patch('outbound_tasks.agent_handle_planned_flow')
def test_publish(agent_handle_planned_flow_mock):
    # Arrange
    flow_data = Mock()

    # Act
    AgentFlowPublisher.publish(flow_data)

    # Assert
    agent_handle_planned_flow_mock.delay.assert_called_with(flow_data)
