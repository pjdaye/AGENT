from unittest.mock import patch, Mock
from clients.form_expert_client import FormExpertClient


class ResponseStub:
    def __init__(self, status_code):
        self.status_code = status_code

    def json(self):
        response_json = {
            'some_label_key': 'label_from_form_expert'
        }
        return response_json


class TwoWidgetResponseStub:
    def __init__(self, status_code):
        self.status_code = status_code

    def json(self):
        response_json = {
            'some_label_key_1': 'label_from_form_expert_1',
            'some_label_key_2': 'label_from_form_expert_2'
        }
        return response_json


class NoneResponseStub:
    def __init__(self, status_code):
        self.status_code = status_code

    def json(self):
        response_json = {
            'some_label_key': None
        }
        return response_json


def test_form_expert_client_sets_service_url_from_environment_on_instantiation():
    # Arrange and Act
    with patch('Clients.page_analysis_client.os.environ') as mock_environment:
        environment = {'FORM_EXPERT_URL': 'url_from_environment'}
        mock_environment.__contains__.return_value = True
        mock_environment.__getitem__.side_effect = environment.__getitem__
        form_expert_client = FormExpertClient()

    # Assert
    assert form_expert_client.FORM_EXPERT_URL == 'url_from_environment'


def test_get_concrete_values_returns_empty_list_given_no_widgets():
    # Arrange
    widgets = []
    form_expert_client = FormExpertClient()

    # Act
    with patch('Clients.form_expert_client.requests.post') as mock_post_request:
        mock_post_request.return_value = ResponseStub(status_code=200)
        result = form_expert_client.get_concrete_values(widgets)

    # Assert
    assert result == []


def test_get_concrete_values_makes_appropriate_post_request_with_no_widgets():
    # Arrange
    widgets = []
    form_expert_client = FormExpertClient()

    # Act
    with patch('Clients.form_expert_client.requests.post') as mock_post_request:
        mock_post_request.return_value = ResponseStub(status_code=200)
        form_expert_client.get_concrete_values(widgets)

    # Assert
    url = 'http://form-expert/api/v1/fill_form'
    mock_post_request.assert_called_once_with(url, json=widgets, verify=False)


def test_get_concrete_values_returns_label_from_form_expert_with_one_widget():
    # Arrange
    widget = {
        'label': 'some_label',
        'label_key': 'some_label_key'
    }
    widgets = [widget]
    form_expert_client = FormExpertClient()

    # Act
    with patch('Clients.form_expert_client.requests.post') as mock_post_request:
        mock_post_request.return_value = ResponseStub(status_code=200)
        results = form_expert_client.get_concrete_values(widgets)

    # Assert
    assert results == [{'label': 'some_label', 'label_key': 'some_label_key', 'value': 'label_from_form_expert'}]


def test_get_concrete_values_returns_label_from_form_expert_with_two_widgets():
    # Arrange
    widgets = [
        {
            'label': 'some_label_1',
            'label_key': 'some_label_key_1'
        },
        {
            'label': 'some_label_2',
            'label_key': 'some_label_key_2'
        }
    ]
    form_expert_client = FormExpertClient()

    # Act
    with patch('Clients.form_expert_client.requests.post') as mock_post_request:
        mock_post_request.return_value = TwoWidgetResponseStub(status_code=200)
        result = form_expert_client.get_concrete_values(widgets)

    # Assert
    assert result == [{'label': 'some_label_1', 'label_key': 'some_label_key_1', 'value': 'label_from_form_expert_1'},
                      {'label': 'some_label_2', 'label_key': 'some_label_key_2', 'value': 'label_from_form_expert_2'}]


def test_get_concrete_values_calls_fallback_for_a_single_label_that_is_not_in_form_expert_response():
    # Arrange
    widgets = [
        {
            'label': 'some_label',
            'label_key': 'some_weird_label_key'
        }
    ]
    form_expert_client = FormExpertClient()
    form_expert_client.fallback = Mock(return_value='fallback_value')

    # Act
    with patch('Clients.form_expert_client.requests.post') as mock_post_request:
        mock_post_request.return_value = ResponseStub(status_code=200)
        form_expert_client.get_concrete_values(widgets)

    # Assert
    form_expert_client.fallback.assert_called_with('some_label')


def test_get_concrete_values_calls_fallback_for_a_single_label_that_is_none_in_form_expert_response():
    # Arrange
    widgets = [
        {
            'label': 'some_label',
            'label_key': 'some_label_key'
        }
    ]
    form_expert_client = FormExpertClient()
    form_expert_client.fallback = Mock(return_value='fallback_value')

    # Act
    with patch('Clients.form_expert_client.requests.post') as mock_post_request:
        mock_post_request.return_value = NoneResponseStub(status_code=200)
        form_expert_client.get_concrete_values(widgets)

    # Assert
        form_expert_client.fallback.assert_called_with('some_label')


def test_get_concrete_value_returns_fallback_value_when_form_expert_response_is_not_200():
    # Arrange
    label_key = 'some_label_key'
    form_expert_client = FormExpertClient()
    form_expert_client.fallback = Mock(return_value='fallback_value')

    # Act
    with patch('Clients.form_expert_client.requests.post') as mock_post_request:
        mock_post_request.return_value = ResponseStub(status_code=404)
        result = form_expert_client.get_concrete_value(label_key)

    # Assert
    assert result == 'fallback_value'


def test_get_concrete_value_returns_fallback_value_when_label_is_not_in_form_expert_response():
    # Arrange
    label_key = 'some_weird_label_key'
    form_expert_client = FormExpertClient()
    form_expert_client.fallback = Mock(return_value='fallback_value')

    # Act
    with patch('Clients.form_expert_client.requests.post') as mock_post_request:
        mock_post_request.return_value = ResponseStub(status_code=200)
        result = form_expert_client.get_concrete_value(label_key)

    # Assert
    assert result == 'fallback_value'


def test_get_concrete_value_returns_fallback_value_when_form_expert_result_is_none():
    # Arrange
    label_key = 'some_label_key'
    form_expert_client = FormExpertClient()
    form_expert_client.fallback = Mock(return_value='fallback_value')

    # Act
    with patch('Clients.form_expert_client.requests.post') as mock_post_request:
        mock_post_request.return_value = NoneResponseStub(status_code=200)
        result = form_expert_client.get_concrete_value(label_key)

    # Assert
    assert result == 'fallback_value'


def test_get_concrete_value_returns_label_from_form_expert_with_successful_request_and_known_label():
    # Arrange
    label_key = 'some_label_key'
    form_expert_client = FormExpertClient()

    # Act
    with patch('Clients.form_expert_client.requests.post') as mock_post_request:
        mock_post_request.return_value = ResponseStub(status_code=200)
        result = form_expert_client.get_concrete_value(label_key)

    # Assert
    assert result == 'label_from_form_expert'


