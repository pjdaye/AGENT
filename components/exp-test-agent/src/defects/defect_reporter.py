"""Responsible for reporting defects found during exploration and testing."""

from defects.defect import Defect


class DefectReporter:
    """Responsible for reporting defects found during exploration and testing."""

    def __init__(self):
        """ Initializes the DefectReporter class.
        """
        self.defects = []

    def add_defect(self, flow, flow_actions, failure_index):
        """ Adds a defect to an internal list of tracked defects.

        :param flow: The abstract test flow that resulted in this defect.
        :param flow_actions: The actions associated with the abstract test flow.
        :param failure_index: The index within the flow_actions list where the failure occurred.
        """

        self.defects.append(Defect(flow, flow_actions, failure_index))

    def report_defects(self):
        """ Reports the defects found during exploration and testing.
        """

        # TODO: Not yet implemented.
