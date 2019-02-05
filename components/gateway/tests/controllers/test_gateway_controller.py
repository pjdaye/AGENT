from unittest.mock import call, Mock, patch

from controllers.gateway_controller import GatewayController


def test_add_routes():
    # Arrange
    app = Mock()
    gateway_controller = GatewayController(app)

    # Act
    gateway_controller.add_routes()

    # Assert
    app.route.assert_has_calls(
        [
            call('/v1/status', method='GET', callback=gateway_controller.get_status),
            call('/v1/start', method='POST', callback=gateway_controller.start_session),
            call('/v1/stop', method='POST', callback=gateway_controller.stop_session)
        ]
    )


@patch(GatewayController.__module__ + '.bottle')
def test_get_status(bottle_mock):
    # Arrange
    app = Mock()
    gateway_controller = GatewayController(app)

    # Act
    gateway_controller.get_status()

    # Assert
    bottle_mock.HTTPResponse.assert_called_with(body={'status': 'OK'}, status=200)


@patch(GatewayController.__module__ + '.GatewayService')
@patch(GatewayController.__module__ + '.request')
@patch(GatewayController.__module__ + '.bottle')
def test_start_session(bottle_mock, request_mock, gateway_service_constructor_mock):
    # Arrange
    app = Mock()
    request_payload_mock = Mock()
    request_mock.json = request_payload_mock
    session_mock = Mock()
    gateway_service_mock = Mock()
    gateway_service_constructor_mock.return_value = gateway_service_mock
    gateway_service_mock.start_session.return_value = session_mock
    gateway_controller = GatewayController(app)

    # Act
    gateway_controller.start_session()

    # Assert
    gateway_service_mock.start_session.assert_called_with(request_payload_mock)
    bottle_mock.HTTPResponse.assert_called_with(body=session_mock, status=200)


@patch(GatewayController.__module__ + '.GatewayService')
@patch(GatewayController.__module__ + '.bottle')
def test_stop_session(bottle_mock, gateway_service_constructor_mock):
    # Arrange
    app = Mock()
    response_mock = Mock()
    gateway_service_mock = Mock()
    gateway_service_constructor_mock.return_value = gateway_service_mock
    gateway_service_mock.stop_session.return_value = response_mock
    gateway_controller = GatewayController(app)

    # Act
    gateway_controller.stop_session()

    # Assert
    gateway_service_mock.stop_session.assert_called_with()
    bottle_mock.HTTPResponse.assert_called_with(body=response_mock, status=200)
