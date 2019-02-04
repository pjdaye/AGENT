from unittest.mock import patch
from clients.flow_generation_client import FlowGeneratorClient


class EmptySequenceResponseStub:
    def __init__(self, status_code):
        self.status_code = status_code

    def json(self):
        return {
            'sequences': []
        }


class SingleSequenceResponseStub:
    def __init__(self, status_code):
        self.status_code = status_code

    def json(self):
        return {
            'sequences': [['Observe', 'TextBox', 'FirstName', 'Expansion1', 'Expansion2']]
        }


def test_flow_generation_client_sets_service_url_from_environment_on_instantiation():
    # Arrange and Act
    with patch('os.environ') as mock_environment:
        environment = {'FLOW_GENERATION_URL': 'url_from_environment'}
        mock_environment.__contains__.return_value = True
        mock_environment.__getitem__.side_effect = environment.__getitem__
        flow_generation_client = FlowGeneratorClient()

    # Assert
    assert flow_generation_client.SERVICE_URL == 'url_from_environment'


def test_flow_generation_client_makes_post_request_with_url_and_query():
    # Arrange
    flow_generation_client = FlowGeneratorClient()
    original_query = "Observe Textbox FirstName"
    call_query = ['observe', 'textbox', 'firstname']
    url = 'http://flow-generator/v1/predict'

    # Act
    with patch('requests.post') as mock_post_request:
        mock_post_request.return_value = EmptySequenceResponseStub(status_code=200)
        flow_generation_client.generate_flow(original_query)

    # Assert
    mock_post_request.assert_called_with(url, json=call_query, verify=False)


def test_flow_generation_client_returns_none_on_successful_response_and_no_sequences():
    # Arrange
    flow_generation_client = FlowGeneratorClient()
    query = 'Observe Textbox FirstName'

    # Act
    with patch('requests.post') as mock_post_request:
        mock_post_request.return_value = EmptySequenceResponseStub(status_code=200)
        flow = flow_generation_client.generate_flow(query)

    # Assert
    assert flow is None


def test_flow_generation_client_returns_expanded_sequence_on_successful_response_and_one_sequence():
    # Arrange
    flow_generation_client = FlowGeneratorClient()
    query = 'Observe Textbox FirstName'

    # Act
    with patch('requests.post') as mock_post_request:
        mock_post_request.return_value = SingleSequenceResponseStub(status_code=200)
        flow = flow_generation_client.generate_flow(query)

    # Assert
    assert flow == 'OBSERVE TEXTBOX FIRSTNAME EXPANSION1 EXPANSION2'


def test_flow_generation_client_returns_false_when_response_is_not_200():
    # Arrange
    flow_generation_client = FlowGeneratorClient()
    query = 'Observe Textbox FirstName'

    # Act
    with patch('requests.post') as mock_post_request:
        mock_post_request.return_value = EmptySequenceResponseStub(status_code=404)
        flow = flow_generation_client.generate_flow(query)

    # Assert
    assert flow is False




