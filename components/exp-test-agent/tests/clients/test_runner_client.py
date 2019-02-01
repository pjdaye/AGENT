from unittest.mock import Mock, patch, mock_open

import pytest
from aeoncloud.exceptions.aeon_session_error import AeonSessionError

from Clients.runner_client import RunnerClient


@pytest.fixture
def runner_client():
    mock_open_func = mock_open(read_data='some_data')
    with patch('builtins.open', mock_open_func):
        mock_runner_client = RunnerClient('runner_url')

    mock_runner_client.aeon = Mock()
    mock_runner_client.session = Mock()
    return mock_runner_client


@patch('Clients.runner_client.LOGGER')
def test_runner_client_launch_returns_true_on_success(_, runner_client):
    # Arrange

    # Act
    result = runner_client.launch('some_url')

    # Assert
    assert result is True


@patch('Clients.runner_client.LOGGER')
def test_runner_client_launch_returns_false_on_failed_navigation(_, runner_client):
    # Arrange
    runner_client.navigate = Mock(return_value=False)

    # Act
    result = runner_client.launch('some_url')

    # Assert
    assert result is False


@patch('Clients.runner_client.LOGGER')
def test_runner_client_launch_returns_false_on_aeon_session_error_from_navigate_call(_, runner_client):
    # Arrange
    runner_client.navigate = Mock()
    runner_client.navigate.side_effect = AeonSessionError()

    # Act
    result = runner_client.launch('some_url')

    # Assert
    assert result is False


@patch('Clients.runner_client.LOGGER')
def test_runner_client_launch_returns_false_on_aeon_session_error_from_get_session_call(_, runner_client):
    # Arrange
    runner_client.aeon.get_session.side_effect = AeonSessionError()

    # Act
    result = runner_client.launch('some_url')

    # Assert
    assert result is False


@patch('Clients.runner_client.LOGGER')
def test_runner_client_navigate_returns_false_on_execute_command_error(_, runner_client):
    # Arrange
    runner_client.session.execute_command.side_effect = AeonSessionError()

    # Act
    result = runner_client.navigate('some_url')

    # Assert
    assert result is False


@patch('Clients.runner_client.LOGGER')
def test_perform_set_action_returns_true_on_success(_, runner_client):
    # Arrange
    selector = 'some_selector'
    action = 'set'

    # Act
    result = runner_client.perform_action(selector, action)

    # Assert
    assert result is True


@patch('Clients.runner_client.LOGGER')
def test_perform_click_action_returns_true_on_success(_, runner_client):
    # Arrange
    selector = 'some_selector'
    action = 'click'

    # Act
    result = runner_client.perform_action(selector, action)

    # Assert
    assert result is True

@patch('Clients.runner_client.LOGGER')
def test_perform_set_action_executes_set_command(_, runner_client):
    # Arrange
    selector = 'some_selector'
    action = 'set'
    value = 'some_value'

    # Act
    runner_client.perform_action(selector, action, value)

    # Assert
    """call_args[0][0] contains the first argument execute_command was called with
    https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.call_args"""
    command = runner_client.session.execute_command.call_args[0][0]
    assert command == 'SetCommand'


@patch('Clients.runner_client.LOGGER')
def test_perform_click_action_executes_click_command(_, runner_client):
    # Arrange
    selector = 'some_selector'
    action = 'click'

    # Act
    runner_client.perform_action(selector, action)

    # Assert
    """call_args[0][0] contains the first argument execute_command was called with
    https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.call_args"""
    command = runner_client.session.execute_command.call_args[0][0]
    assert command == 'ClickCommand'


@patch('Clients.runner_client.LOGGER')
def test_perform_unknown_action_returns_false(_, runner_client):
    # Arrange
    selector = 'some_selector'
    action = 'unknown'

    # Act
    result = runner_client.perform_action(selector, action)

    # Assert
    assert result is False


@patch('Clients.runner_client.LOGGER')
def test_perform_action_returns_false_on_aeon_session_error(_, runner_client):
    # Arrange
    selector = 'some_selector'
    action = 'set'
    runner_client.session.execute_command.side_effect = AeonSessionError()

    # Act
    result = runner_client.perform_action(selector, action)

    # Assert
    assert result is False


@patch('Clients.runner_client.LOGGER')
def test_concrete_state_returns_false_when_get_document_location_script_fails(_, runner_client):
    # Arrange
    def command_side_effect(*args):
        if args[0] == 'ExecuteScriptCommand':
            return {'success': False, 'failureMessage': 'message'}
        return {'success': True}

    runner_client.session.execute_command.side_effect = command_side_effect

    # Act
    result = runner_client.concrete_state()

    # Assert
    assert result is False


@patch('Clients.runner_client.LOGGER')
def test_concrete_state_returns_empty_concrete_state_when_page_is_xml(_, runner_client):
    # Arrange
    def command_side_effect():
        response  = {
            'success': True,
            'data': 'document.xml'
        }
        return response

    runner_client.session.execute_command.side_effect = command_side_effect

    # Act
    result = runner_client.concrete_state()

    # Assert
    expected_response = {
        'url': 'document.xml',
        'title': 'document.xml',
        'widgets': {},
        'root': 'HTML0_0:0'
    }
    assert result == expected_response


@patch('Clients.runner_client.LOGGER')
def test_concrete_state_returns_empty_concrete_state_when_page_is_json(_, runner_client):
    # Arrange
    def command_side_effect(*args):
        response = {
            'success': True,
            'data': 'document.json'
        }
        return response

    runner_client.session.execute_command.side_effect = command_side_effect

    # Act
    result = runner_client.concrete_state()

    # Assert
    expected_response = {
        'url': 'document.json',
        'title': 'document.json',
        'widgets': {},
        'root': 'HTML0_0:0'
    }
    assert result == expected_response


@patch('Clients.runner_client.LOGGER')
def test_concrete_state_returns_false_when_has_jquery_script_failed(_, runner_client):
    # Arrange
    runner_client.HAS_JQUERY_SCRIPT = 'has_jquery_script'

    def command_side_effect(*args):
        if args[0] == 'ExecuteScriptCommand' and args[1] == [runner_client.HAS_JQUERY_SCRIPT]:
            return {'success': False, 'failureMessage': 'message'}

        return {'success': True, 'data': 'some_data'}

    runner_client.session.execute_command.side_effect = command_side_effect

    # Act
    result = runner_client.concrete_state()

    # Assert
    assert result is False


@patch('Clients.runner_client.LOGGER')
def test_concrete_state_injects_query_when_page_does_not_have_jquery(_, runner_client):
    # Arrange
    runner_client.HAS_JQUERY_SCRIPT = 'has_jquery'

    def command_side_effect(*args):
        if args[0] == 'ExecuteScriptCommand' and args[1] == [runner_client.HAS_JQUERY_SCRIPT]:
            response = {
                'success': True,
                'data': 'false'
            }
            return response

        return {
            'success': True,
            'data': 'true'
        }

    runner_client.session.execute_command.side_effect = command_side_effect
    runner_client.JQUERY_SCRIPT = 'jquery_script'

    # Act
    runner_client.concrete_state()

    # Assert
    runner_client.session.execute_command.assert_any_call('ExecuteAsyncScriptCommand', [runner_client.JQUERY_SCRIPT])


@patch('Clients.runner_client.LOGGER')
def test_concrete_state_returns_false_when_jquery_injection_fails(_, runner_client):
    # Arrange
    runner_client.JQUERY_SCRIPT = 'jquery'

    def command_side_effect(*args):
        if args[0] == 'ExecuteAsyncScriptCommand' and args[1] == [runner_client.JQUERY_SCRIPT]:
            response = {
                'success': False,
                'failureMessage': 'failure message'
            }
            return response
        elif args[0] == 'ExecuteScriptCommand' and args[1] == [runner_client.HAS_JQUERY_SCRIPT]:
            response = {
                'success': True,
                'data': 'false'
            }
            return response

        return {
            'success': True,
            'data': 'true'
        }

    runner_client.session.execute_command.side_effect = command_side_effect

    # Act
    result = runner_client.concrete_state()

    # Assert
    assert result is False


@patch('Clients.runner_client.LOGGER')
def test_concrete_state_returns_false_when_fix_jquery_script_fails(_, runner_client):
    # Arrange
    runner_client.FIX_JQUERY_SCRIPT = 'fix_script'

    def command_side_effect(*args):
        if args[0] == 'ExecuteScriptCommand' and args[1] == [runner_client.FIX_JQUERY_SCRIPT]:
            response = {
                'success': False,
                'failureMessage': 'some_message'
            }
            return response

        return {
            'success': True,
            'data': 'true'
        }

    runner_client.session.execute_command.side_effect = command_side_effect

    # Act
    result = runner_client.concrete_state()

    # Assert
    assert result is False


@patch('Clients.runner_client.LOGGER')
def test_concrete_state_returns_false_when_dom_is_not_loaded(_, runner_client):
    # Arrange
    runner_client.CHECK_READY_SCRIPT = 'check_ready_script'

    def command_side_effect(*args):
        if args[0] == 'ExecuteAsyncScriptCommand' and args[1] == [runner_client.CHECK_READY_SCRIPT]:
            response = {
                'success': False,
                'failureMessage': 'some_message'
            }
            return response

        return {
            'success': True,
            'data': 'true'
        }

    runner_client.session.execute_command.side_effect = command_side_effect

    # Act
    result = runner_client.concrete_state()

    # Assert
    assert result is False


@patch('Clients.runner_client.LOGGER')
def test_concrete_state_returns_false_when_execute_scrape_script_fails(_, runner_client):
    # Arrange
    runner_client.SCRAPE_SCRIPT = 'scrape'

    def command_side_effect(*args):
        if args[0] == 'ExecuteScriptCommand' and args[1] == [runner_client.SCRAPE_SCRIPT]:
            response = {
                'success': False,
                'failureMessage': 'some_message'
            }
            return response

        return {
            'success': True,
            'data': 'true'
        }

    runner_client.session.execute_command.side_effect = command_side_effect

    # Act
    result = runner_client.concrete_state()

    # Assert
    assert result is False


@patch('Clients.runner_client.LOGGER')
def test_concrete_state_returns_false_when_aeon_session_error_occurs(_, runner_client):
    # Arrange
    runner_client.session.execute_command.side_effect = AeonSessionError()

    # Act
    result = runner_client.concrete_state()

    # Assert
    assert result is False