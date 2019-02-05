from unittest.mock import patch, call, Mock

from agent_celery import main


@patch('agent_celery.threading.Thread')
@patch('agent_celery.uuid.uuid4')
@patch('agent_celery.celery.worker.WorkController')
@patch('agent_celery.create_app')
@patch('agent_celery.LOGGER')
def test_coordinator_celery(
        logger_mock,
        create_app_mock,
        work_controller_mock,
        uuid4_method_mock,
        thread_mock
):
    # Arrange
    create_app_mock_return_value = Mock()
    create_app_mock.return_value = create_app_mock_return_value
    work_controller_mock_return_value = Mock()
    work_controller_mock.return_value = work_controller_mock_return_value
    uuid4_mock = Mock()
    uuid4_mock.hex = 'test-hex'
    uuid4_method_mock.return_value = uuid4_mock
    thread_mock_return_value = Mock()
    thread_mock.return_value = thread_mock_return_value

    # Act
    main()

    # Assert
    logger_mock.info.assert_has_calls(
        [
            call("Starting agent..."),
            call("Celery started."),
            call("Agent started.")
        ]
    )
    create_app_mock.assert_called_with(['inbound_tasks', 'outbound_tasks'])
    work_controller_mock.assert_called_with(
        app=create_app_mock_return_value,
        hostname='test-agent-test-hex',
        pool_cls='solo',
        queues=['test_agent_queue', 'agent_broadcast_tasks']
    )
    thread_mock.assert_called_with(target=work_controller_mock_return_value.start)
    thread_mock_return_value.start.assert_called_with()
