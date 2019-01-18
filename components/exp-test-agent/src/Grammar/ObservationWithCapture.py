from Grammar.Observation import Observation


class ObservationWithCapture(Observation):
    def __init__(self):
        super().__init__()
        self.variable = None

    def with_capture(self, variable):
        self.variable = variable
        return self

    def __str__(self):
        output = "{} {}".format(super().__str__(), str(self.variable))
        return output
