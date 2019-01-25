

class NotCapture:
    def __init__(self, variable):
        self.variable = variable

    def __str__(self):
        return "!{}".format(self.variable)
