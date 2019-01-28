from aist_common.grammar.observation import Observation


class ObservationInCollection(Observation):
    def __init__(self):
        super().__init__()
        self.capture = None

    def with_capture(self, capture):
        self.capture = capture

    def __str__(self):
        output = "OBSERVE" if self.observe else "NOTOBSERVE"
        if self.capture:
            output += " " + str(self.capture)
        output += " IN COLLECTION"
        return output
