

class ComponentActionList:
    def __init__(self, actions):
        self.actions = actions

    def insert_action(self, action):
        self.actions.insert(0, action)

    def __len__(self):
        return len(self.actions)

    def __iter__(self):
        return self.actions

    def __str__(self):
        return " ".join([str(obs) for obs in self.actions])
