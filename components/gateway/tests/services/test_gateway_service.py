from unittest.mock import patch

from services.gateway_service import GatewayService


@patch(GatewayService.__module__ + '.create_app')
@patch(GatewayService.__module__ + '.LOGGER')
def test_start_session(logger_mock, create_app_mock):
    # Arrange
    request_payload = {
        'SUT_URL': 'sut_url'
    }

    # Act
    result = GatewayService.start_session(request_payload)

    # Assert
    # Cannot verify that nested method 'start_agent_session' was accessed
    # because it is in local scope only
    create_app_mock.assert_called_with([])
    logger_mock.info.assert_called_with('Signaling agents to start exploring: sut_url')
    assert len(result['session']) == 32


@patch(GatewayService.__module__ + '.create_app')
@patch(GatewayService.__module__ + '.LOGGER')
def test_stop_session(logger_mock, create_app_mock):
    # Arrange

    # Act
    result = GatewayService.stop_session()

    # Assert
    # Cannot verify that nested method 'stop_agent_session' was accessed
    # because it is in local scope only
    create_app_mock.assert_called_with([])
    logger_mock.info.assert_called_with('Signaling agents to stop exploration.')
    assert result['stopped'] is True
