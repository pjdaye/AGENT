"""Represents an issue found during exploration and testing."""


class Defect:
    """Represents an issue found during exploration and testing."""

    def __init__(self, flow, flow_actions, failure_index):
        """ Initializes the Defect class.

        :param flow: The abstract test flow that resulted in this defect.
        :param flow_actions: The actions associated with the abstract test flow.
        :param failure_index: The index within the flow_actions list where the failure occurred.
        """

        self.flow = flow
        self.flow_actions = flow_actions
        self.failure_index = failure_index

