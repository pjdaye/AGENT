"""Represents a concrete test flow."""


class ConcreteTestFlow:
    """Represents a concrete test flow."""

    def __init__(self, path, abstract_state, flow, bound_actions):
        """ Initializes the ConcreteTestFlow class.

        :param path: The interactions that were taken that led to the abstract state from which this flow begins.
        :param abstract_state: The abstract state for which this flow begins.
        :param flow: The abstract flow this concrete flow is being created from.
        :param bound_actions: The actions that must be executed as part of this concrete test flow.
        """

        self.path = path
        self.initial_state = abstract_state
        self.original_flow = flow
        self.bound_actions = bound_actions
        self.hash = 0

    def calculate_hash(self):
        """ Calculates a hash for the concrete flow that is comprised of the source state
            hash, all bound actions, and all post-condition observation steps.
        """

        to_hash = ()
        to_hash += (self.initial_state.hash,)
        for bound_action in self.bound_actions:
            component_action = bound_action[0]
            bound_widget = bound_action[1]
            to_hash += (str(component_action),)
            to_hash += (str(bound_widget['key']),)
        for observe_step in self.original_flow.observe.observations:
            to_hash += (str(observe_step),)
        self.hash = hash(frozenset(to_hash))
