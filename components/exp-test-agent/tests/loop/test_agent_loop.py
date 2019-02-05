from abstraction.actionable_state import ActionableState
from loop.agent_loop import AgentLoop
from unittest.mock import Mock, patch


@patch(AgentLoop.__module__ + '.threading.Thread')
def test_agent_start(thread):
    # Arrange.
    sut_url = "TEST"
    runner_url = "TEST"
    form_expert_client = Mock()
    runner_client = Mock()
    page_analysis_client = Mock()
    flow_generator_client = Mock()

    loop = AgentLoop(sut_url, runner_url, form_expert_client, runner_client,
                     page_analysis_client, flow_generator_client)

    thread_mock = Mock()
    thread.return_value = thread_mock

    # Act.
    loop.start()

    # Assert.
    assert thread.called
    assert thread_mock.start.called


@patch.dict(AgentLoop.__module__ + '.general_memory', {'SESSION_STOPPED': False}, clear=True)
def test_loop_start():
    # Arrange.
    sut_url = "TEST"
    runner_url = "TEST"
    form_expert_client = Mock()
    runner_client = Mock()
    page_analysis_client = Mock()
    flow_generator_client = Mock()

    loop = AgentLoop(sut_url, runner_url, form_expert_client, runner_client,
                     page_analysis_client, flow_generator_client)

    # Act.
    with patch(AgentLoop.__module__ + '.AgentLoop.loop_iteration') as loop_iteration:
        with patch(AgentLoop.__module__ + '.AgentLoop.loop_end') as loop_end:
            loop.loop_start()

    # Assert.
    assert runner_client.launch.called_with(sut_url)
    assert loop_iteration.call_count == AgentLoop.NUM_ITERATIONS
    assert loop_end.called


@patch.dict(AgentLoop.__module__ + '.general_memory', {'SESSION_STOPPED': True}, clear=True)
def test_session_stop():
    # Arrange.
    sut_url = "TEST"
    runner_url = "TEST"
    form_expert_client = Mock()
    runner_client = Mock()
    page_analysis_client = Mock()
    flow_generator_client = Mock()

    loop = AgentLoop(sut_url, runner_url, form_expert_client, runner_client,
                     page_analysis_client, flow_generator_client)

    # Act.
    with patch(AgentLoop.__module__ + '.AgentLoop.loop_iteration') as loop_iteration:
        with patch(AgentLoop.__module__ + '.AgentLoop.loop_end') as loop_end:
            loop.loop_start()

    # Assert.
    assert runner_client.launch.called_with(sut_url)
    assert not loop_iteration.called
    assert loop_end.called


@patch.dict(AgentLoop.__module__ + '.general_memory', {'SESSION_STOPPED': False}, clear=True)
def test_runner_unable_to_launch():
    # Arrange.
    sut_url = "TEST"
    runner_url = "TEST"
    form_expert_client = Mock()
    runner_client = Mock()
    page_analysis_client = Mock()
    flow_generator_client = Mock()

    runner_client.launch.return_value = False

    loop = AgentLoop(sut_url, runner_url, form_expert_client, runner_client,
                     page_analysis_client, flow_generator_client)

    # Act.
    with patch(AgentLoop.__module__ + '.AgentLoop.loop_iteration') as loop_iteration:
        with patch(AgentLoop.__module__ + '.AgentLoop.loop_end') as loop_end:
            loop.loop_start()

    # Assert.
    assert runner_client.launch.called_with(sut_url)
    assert not loop_iteration.called
    assert not loop_end.called


def test_loop_end():
    # Arrange.
    sut_url = "TEST"
    runner_url = "TEST"
    form_expert_client = Mock()
    runner_client = Mock()
    page_analysis_client = Mock()
    flow_generator_client = Mock()

    loop = AgentLoop(sut_url, runner_url, form_expert_client, runner_client,
                     page_analysis_client, flow_generator_client)

    # Act.
    loop.loop_end()

    # Assert.
    assert runner_client.quit.called


@patch.dict(AgentLoop.__module__ + '.general_memory', {'SESSION_STOPPED': False}, clear=True)
def test_loop_lifecycle():
    # Arrange.
    sut_url = "TEST"
    runner_url = "TEST"
    form_expert_client = Mock()
    runner_client = Mock()
    page_analysis_client = Mock()
    flow_generator_client = Mock()

    loop = AgentLoop(sut_url, runner_url, form_expert_client, runner_client,
                     page_analysis_client, flow_generator_client)

    # Act.
    with patch(AgentLoop.__module__ + '.AgentLoop.loop_iteration') as loop_iteration:
        loop.loop_start()

    # Assert.
    assert runner_client.launch.called_with(sut_url)
    assert loop_iteration.call_count == AgentLoop.NUM_ITERATIONS
    assert runner_client.quit.called


@patch.dict(AgentLoop.__module__ + '.general_memory', {'SESSION_STOPPED': False}, clear=True)
def test_loop_iteration_exception():
    # Arrange.
    sut_url = "TEST"
    runner_url = "TEST"
    form_expert_client = Mock()
    runner_client = Mock()
    page_analysis_client = Mock()
    flow_generator_client = Mock()

    loop = AgentLoop(sut_url, runner_url, form_expert_client, runner_client,
                     page_analysis_client, flow_generator_client)

    # Act.
    with patch(AgentLoop.__module__ + '.AgentLoop.loop_iteration') as loop_iteration:
        with patch(AgentLoop.__module__ + '.AgentLoop.loop_end') as loop_end:
            def exception_side_effect():
                raise Exception('test')

            loop_iteration.side_effect = exception_side_effect

            loop.loop_start()

    # Assert.
    assert runner_client.launch.called_with(sut_url)
    assert loop_iteration.call_count == 1
    assert loop_end.called


def test_loop_iteration_happy_path():
    # Arrange.
    sut_url = "TEST"
    runner_url = "TEST"
    form_expert_client = Mock()
    runner_client = Mock()
    page_analysis_client = Mock()
    flow_generator_client = Mock()

    page_analysis = {
        'analysis': {
            'labelCandidates': ['Label_FirstName'],
            'COMMIT': ['C1'],
            'ERRORMESSAGE': ['E1'],
            'errorMessages': ['E1']
        }
    }

    page_analysis_client.run_analysis.return_value = page_analysis

    widget_first_name_label = {
        'key': 'Label_FirstName',
        'label': 'FirstNameLabel',
        'actions': [],
        'selector': '#lblFirstName',
        'properties': {
            'tagName': 'LABEL',
            'text': 'First Name',
            'x': 10,
            'y': 10
        }
    }

    widget_first_name = {
        'key': 'FIRSTNAME',
        'label': 'FirstName',
        'actions': ['set'],
        'selector': '#firstName',
        'properties': {
            'tagName': 'INPUT',
            'x': 20,
            'y': 20
        }
    }

    widget_save = {
        'key': 'C1',
        'label': 'Save',
        'actions': ['click'],
        'selector': '#save',
        'properties': {
            'tagName': 'BUTTON',
            'x': 40,
            'y': 40
        }
    }

    widget_error = {
        'key': 'E1',
        'label': 'Error',
        'properties': {
            'tagName': 'LABEL',
            'x': 60,
            'y': 60
        }
    }

    target_concrete_state = {
        'widgets': {
            'Label_FirstName': widget_first_name_label,
            'FIRSTNAME': widget_first_name,
            'C1': widget_save,
            'E1': widget_error
        }
    }

    flow_generator_client.generate_flow.return_value = "OBSERVE TEXTBOX FIRSTNAME " \
                                                       "TRY VALID FIRSTNAME " \
                                                       "CLICK COMMIT " \
                                                       "NOTOBSERVE ERRORMESSAGE"

    runner_client.concrete_state.return_value = target_concrete_state

    flow_publisher = Mock()

    flow_executor = Mock()

    loop = AgentLoop(sut_url, runner_url, form_expert_client, runner_client,
                     page_analysis_client, flow_generator_client, flow_publisher, flow_executor)

    # Act.
    with patch(AgentLoop.__module__ + '.PriorityMemory') as memory_mock:
        actual_memory_mock = Mock()
        memory_mock.return_value = actual_memory_mock

        loop.loop_iteration()

        # Assert.
        assert flow_generator_client.generate_flow.called
        assert flow_publisher.publish.call_count == 2
        assert flow_executor.execute.call_count == 1
        assert not actual_memory_mock.in_memory.called


def test_loop_iteration_no_generated_test_flows_should_explore():
    # Arrange.
    sut_url = "TEST"
    runner_url = "TEST"
    form_expert_client = Mock()
    runner_client = Mock()
    page_analysis_client = Mock()
    flow_generator_client = Mock()

    page_analysis = {
        'analysis': {
            'labelCandidates': ['Label_FirstName'],
            'COMMIT': ['C1'],
            'ERRORMESSAGE': ['E1'],
            'errorMessages': ['E1']
        }
    }

    page_analysis_client.run_analysis.return_value = page_analysis

    widget_first_name_label = {
        'key': 'Label_FirstName',
        'label': 'FirstNameLabel',
        'actions': [],
        'selector': '#lblFirstName',
        'properties': {
            'tagName': 'LABEL',
            'text': 'First Name',
            'x': 10,
            'y': 10
        }
    }

    widget_first_name = {
        'key': 'FIRSTNAME',
        'label': 'FirstName',
        'actions': ['set'],
        'selector': '#firstName',
        'properties': {
            'tagName': 'INPUT',
            'x': 20,
            'y': 20
        }
    }

    widget_save = {
        'key': 'C1',
        'label': 'Save',
        'actions': ['click'],
        'selector': '#save',
        'properties': {
            'tagName': 'BUTTON',
            'x': 40,
            'y': 40
        }
    }

    widget_error = {
        'key': 'E1',
        'label': 'Error',
        'properties': {
            'tagName': 'LABEL',
            'x': 60,
            'y': 60
        }
    }

    target_concrete_state = {
        'widgets': {
            'Label_FirstName': widget_first_name_label,
            'FIRSTNAME': widget_first_name,
            'C1': widget_save,
            'E1': widget_error
        }
    }

    flow_generator_client.generate_flow.return_value = None

    runner_client.concrete_state.return_value = target_concrete_state

    flow_publisher = Mock()

    flow_executor = Mock()

    # Act.
    with patch(AgentLoop.__module__ + '.PriorityMemory') as memory_mock:
        actual_memory_mock = Mock()
        memory_mock.return_value = actual_memory_mock

        actual_memory_mock.choose_widget.return_value = widget_first_name

        loop = AgentLoop(sut_url, runner_url, form_expert_client, runner_client,
                         page_analysis_client, flow_generator_client, flow_publisher, flow_executor)

        loop.loop_iteration()

        # Assert.
        assert flow_generator_client.generate_flow.called
        assert not flow_publisher.publish.called
        assert not flow_executor.execute.called
        assert actual_memory_mock.in_memory.called
        assert actual_memory_mock.update_memory.called
        assert form_expert_client.get_concrete_value.called
        assert runner_client.perform_action.called


class ConcreteTestFlowStub:
    def __init__(self):
        self.hash = 0

    def calculate_hash(self):
        pass


@patch.dict(AgentLoop.__module__ + '.celery_memory', {'HASH': [ConcreteTestFlowStub()]}, clear=True)
def test_loop_iteration_no_generated_test_flow_but_flows_in_queue():
    # Arrange.
    sut_url = "TEST"
    runner_url = "TEST"
    form_expert_client = Mock()
    runner_client = Mock()
    page_analysis_client = Mock()
    flow_generator_client = Mock()

    page_analysis = {
        'analysis': {
            'labelCandidates': ['Label_FirstName'],
            'COMMIT': ['C1'],
            'ERRORMESSAGE': ['E1'],
            'errorMessages': ['E1']
        }
    }

    page_analysis_client.run_analysis.return_value = page_analysis

    widget_first_name_label = {
        'key': 'Label_FirstName',
        'label': 'FirstNameLabel',
        'actions': [],
        'selector': '#lblFirstName',
        'properties': {
            'tagName': 'LABEL',
            'text': 'First Name',
            'x': 10,
            'y': 10
        }
    }

    widget_first_name = {
        'key': 'FIRSTNAME',
        'label': 'FirstName',
        'actions': ['set'],
        'selector': '#firstName',
        'properties': {
            'tagName': 'INPUT',
            'x': 20,
            'y': 20
        }
    }

    widget_save = {
        'key': 'C1',
        'label': 'Save',
        'actions': ['click'],
        'selector': '#save',
        'properties': {
            'tagName': 'BUTTON',
            'x': 40,
            'y': 40
        }
    }

    widget_error = {
        'key': 'E1',
        'label': 'Error',
        'properties': {
            'tagName': 'LABEL',
            'x': 60,
            'y': 60
        }
    }

    target_concrete_state = {
        'widgets': {
            'Label_FirstName': widget_first_name_label,
            'FIRSTNAME': widget_first_name,
            'C1': widget_save,
            'E1': widget_error
        }
    }

    abstract_state = ActionableState()

    abstract_state.add_static_widget(widget_first_name_label)
    abstract_state.add_widget(widget_first_name)
    abstract_state.add_widget(widget_save)
    abstract_state.add_widget(widget_error)

    abstract_state.hash = "HASH"

    flow_generator_client.generate_flow.return_value = None

    runner_client.concrete_state.return_value = target_concrete_state

    flow_publisher = Mock()

    flow_executor = Mock()

    # Act.
    with patch(AgentLoop.__module__ + '.StateAbstracter') as state_abstracter:
        with patch(AgentLoop.__module__ + '.PriorityMemory') as memory_mock:

            actual_memory_mock = Mock()
            memory_mock.return_value = actual_memory_mock

            actual_mapper = Mock()
            state_abstracter.return_value = actual_mapper

            actual_mapper.process.return_value = abstract_state

            loop = AgentLoop(sut_url, runner_url, form_expert_client, runner_client,
                             page_analysis_client, flow_generator_client, flow_publisher, flow_executor)

            loop.loop_iteration()

            # Assert.
            assert flow_generator_client.generate_flow.called
            assert not flow_publisher.publish.called
            assert flow_executor.execute.called
            assert not actual_memory_mock.in_memory.called
            assert not actual_memory_mock.update_memory.called
            assert not form_expert_client.get_concrete_value.called
            assert not runner_client.perform_action.called
