from unittest.mock import patch, Mock, call

from inbound_tasks import start_session, stop_session, handle_planned_flow


@patch('inbound_tasks.AgentLoop')
@patch('inbound_tasks.general_memory')
@patch.dict('inbound_tasks.os.environ', {'RUNNER_URL': 'runner_url'})
@patch('inbound_tasks.LOGGER')
def test_start_session_with_runner_url_set(logger_mock, general_memory_mock, agent_loop_mock):
    # Arrange
    session_start_data = {
        'SUT_URL': 'sut_url'
    }
    agent_loop_return_value = Mock()
    agent_loop_mock.return_value = agent_loop_return_value

    # Act
    result = start_session(session_start_data)

    # Assert
    logger_mock.info.assert_called_with('Starting session.')
    general_memory_mock.__setitem__.assert_called_with('SESSION_STOPPED', False)
    agent_loop_mock.assert_called_with('sut_url', 'runner_url')
    assert agent_loop_return_value.start.called is True
    assert result is True


@patch('inbound_tasks.AgentLoop')
@patch('inbound_tasks.general_memory')
@patch.dict('inbound_tasks.os.environ', {})
@patch('inbound_tasks.LOGGER')
def test_start_session_with_no_runner_url_set(logger_mock, general_memory_mock, agent_loop_mock):
    # Arrange
    session_start_data = {
        'SUT_URL': 'sut_url'
    }
    agent_loop_return_value = Mock()
    agent_loop_mock.return_value = agent_loop_return_value

    # Act
    result = start_session(session_start_data)

    # Assert
    logger_mock.info.assert_called_with('Starting session.')
    logger_mock.error.assert_called_with(
        'Agent has not been configured with a web runner. Please set the RUNNER_URL environment variable.')
    assert general_memory_mock.__setitem__.called is False
    assert agent_loop_mock.called is False
    assert agent_loop_return_value.start.called is False
    assert result == 'Agent has not been configured with a web runner. Please set the RUNNER_URL environment variable.'


@patch('inbound_tasks.general_memory')
@patch('inbound_tasks.LOGGER')
def test_stop_session(logger_mock, general_memory_mock):
    # Arrange

    # Act
    result = stop_session()

    # Assert
    logger_mock.info.assert_called_with('Stopping session.')
    general_memory_mock.__setitem__.assert_called_with('SESSION_STOPPED', True)
    assert result is True


@patch('inbound_tasks.memory_lock')
@patch('inbound_tasks.celery_memory', {1: ['entry1'], 2: ['entry2', 'entry3'], 3: ['entry4', 'entry5']})
@patch('inbound_tasks.jsonpickle')
@patch('inbound_tasks.LOGGER')
def test_handle_planned_flow_state_hash_not_in_memory(logger_mock, jsonpickle_mock, memory_lock_mock):
    # Arrange
    flow_data = Mock()
    planned_flow_mock = Mock()
    planned_flow_mock.hash = 'planned_flow_mock_hash'
    planned_flow_mock.original_flow = 'planned_flow_mock_original_flow'
    initial_state_mock = Mock()
    initial_state_mock.hash = 4
    planned_flow_mock.initial_state = initial_state_mock
    jsonpickle_mock.decode.return_value = planned_flow_mock

    # Act
    result = handle_planned_flow(flow_data)

    # Assert
    jsonpickle_mock.decode.assert_called_with(flow_data)
    logger_mock.info.assert_called_with('Received abstract test on WORKER QUEUE.')
    logger_mock.debug.assert_has_calls(
        [
            call('(planned_flow_mock_hash) planned_flow_mock_original_flow.'),
            call('Flow Queues:'),
            call('State: 1, |Queue|: 1'),
            call('State: 2, |Queue|: 2'),
            call('State: 3, |Queue|: 2'),
            call('State: 4, |Queue|: 1')
        ]
    )
    assert memory_lock_mock.acquire.called is True
    assert memory_lock_mock.release.called is True
    assert result is True


@patch('inbound_tasks.memory_lock')
@patch('inbound_tasks.celery_memory', {1: ['entry1'], 2: ['entry2', 'entry3'], 3: ['entry4', 'entry5']})
@patch('inbound_tasks.jsonpickle')
@patch('inbound_tasks.LOGGER')
def test_handle_planned_flow_state_hash_in_memory(logger_mock, jsonpickle_mock, memory_lock_mock):
    # Arrange
    flow_data = Mock()
    planned_flow_mock = Mock()
    planned_flow_mock.hash = 'planned_flow_mock_hash'
    planned_flow_mock.original_flow = 'planned_flow_mock_original_flow'
    initial_state_mock = Mock()
    initial_state_mock.hash = 2
    planned_flow_mock.initial_state = initial_state_mock
    jsonpickle_mock.decode.return_value = planned_flow_mock

    # Act
    result = handle_planned_flow(flow_data)

    # Assert
    jsonpickle_mock.decode.assert_called_with(flow_data)
    logger_mock.info.assert_called_with('Received abstract test on WORKER QUEUE.')
    logger_mock.debug.assert_has_calls(
        [
            call('(planned_flow_mock_hash) planned_flow_mock_original_flow.'),
            call('Flow Queues:'),
            call('State: 1, |Queue|: 1'),
            call('State: 2, |Queue|: 3'),
            call('State: 3, |Queue|: 2')
        ]
    )
    assert memory_lock_mock.acquire.called is True
    assert memory_lock_mock.release.called is True
    assert result is True
