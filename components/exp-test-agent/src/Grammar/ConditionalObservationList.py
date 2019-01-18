

class ConditionalObservationList:
    def __init__(self, observations):
        self.observations = observations

    def insert_observation(self, observations):
        self.observations.insert(0, observations)

    def __len__(self):
        return len(self.observations)

    def __iter__(self):
        return self.observations

    def __str__(self):
        return "OR( {} )".format(" , ".join([str(obs) for obs in self.observations]))
