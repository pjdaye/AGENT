from unittest.mock import Mock

from defects.defect import Defect


def test_defect():
    # Arrange
    flow_mock = Mock()
    flow_actions_mock = Mock()
    failure_index_mock = Mock()

    # Act
    defect = Defect(flow_mock, flow_actions_mock, failure_index_mock)

    # Assert
    assert defect.flow == flow_mock
    assert defect.flow_actions == flow_actions_mock
    assert defect.failure_index == failure_index_mock
