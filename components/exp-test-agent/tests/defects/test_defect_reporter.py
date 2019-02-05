from unittest.mock import Mock

from defects.defect_reporter import DefectReporter


def test_add_defect():
    # Arrange
    flow_mock = Mock()
    flow_actions_mock = Mock()
    failure_index_mock = Mock()
    defect_reporter = DefectReporter()

    # Act
    defect_reporter.add_defect(flow_mock, flow_actions_mock, failure_index_mock)

    # Assert
    assert len(defect_reporter.defects) == 1
    assert defect_reporter.defects[0].flow == flow_mock
    assert defect_reporter.defects[0].flow_actions == flow_actions_mock
    assert defect_reporter.defects[0].failure_index == failure_index_mock
