from unittest.mock import patch

from Clients.page_analysis_client import PageAnalysisClient


class ResponseStub:
    def __init__(self, status_code):
        self.status_code = status_code

    def json(self):
        response_json = {
            'analysis': {
                'pageTitles': ['page_title_1'],
                'labelCandidates': ['label_candidate_1'],
                'errorMessages': ['error_message_1'],
                'commits': ['commit_1'],
                'cancels': ['cancel_1']
            }
        }
        return response_json


def test_page_analysis_client_sets_service_url_from_environment_on_instantiation():

    # Arrange and Act
    with patch('Clients.page_analysis_client.os.environ') as mock_environment:
        environment = {'PAGE_ANALYSIS_URL': 'url_from_environment'}
        mock_environment.__contains__.return_value = True
        mock_environment.__getitem__.side_effect = environment.__getitem__
        page_analysis_client = PageAnalysisClient()

    # Assert
    assert page_analysis_client.SERVICE_URL == 'url_from_environment'


def test_page_analysis_client_sends_successful_post_request_with_url_and_concrete_state():
    # Arrange
    page_analysis_client = PageAnalysisClient()
    concrete_state = {'root': 'root'}

    # Act and Assert
    with patch('Clients.page_analysis_client.requests.post') as mock_post_request:
        mock_post_request.return_value = ResponseStub(status_code=200)
        page_analysis_client.run_analysis(concrete_state)

        url = 'http://page-analyzer/v1/pageAnalysis/state/concrete'
        mock_post_request.assert_called_with(url, json=concrete_state, verify=False)


@patch('Clients.page_analysis_client.LOGGER')
def test_page_analysis_client_returns_false_when_post_request_fails(_):
    # Arrange
    page_analysis_client = PageAnalysisClient()
    concrete_state = {'root': 'root'}

    # Act
    with patch('Clients.page_analysis_client.requests.post') as mock_post_request:
        mock_post_request.return_value = ResponseStub(status_code=404)
        result = page_analysis_client.run_analysis(concrete_state)

    # Assert
    assert result is False
