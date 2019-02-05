from unittest.mock import patch, call, Mock

from coordinator_celery import main


@patch('coordinator_celery.threading.Thread')
@patch('coordinator_celery.celery.worker.WorkController')
@patch('coordinator_celery.create_app')
@patch('coordinator_celery.LOGGER')
def test_coordinator_celery(
        logger_mock,
        create_app_mock,
        work_controller_mock,
        thread_mock
):
    # Arrange
    create_app_mock_return_value = Mock()
    create_app_mock.return_value = create_app_mock_return_value
    work_controller_mock_return_value = Mock()
    work_controller_mock.return_value = work_controller_mock_return_value
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
        hostname='test-coordinator',
        pool_cls='solo',
        queues=['test_coordinator_queue']
    )
    thread_mock.assert_called_with(target=work_controller_mock_return_value.start)
    thread_mock_return_value.start.assert_called_with()
