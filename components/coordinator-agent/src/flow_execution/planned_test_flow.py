

class PlannedTestFlow:
    def __init__(self, path, act_state, flow, bound_actions):
        self.path = path
        self.initial_state = act_state
        self.original_flow = flow
        self.bound_actions = bound_actions
        self.hash = 0

    def calculate_hash(self):
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
