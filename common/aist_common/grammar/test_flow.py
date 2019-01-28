

class TestFlow:
    def __init__(self, perceive, act, observe):
        self.perceive = perceive
        self.act = act
        self.observe = observe

    def __str__(self):
        output = ""
        if self.perceive and len(self.perceive) > 0:
            output += str(self.perceive)
        if self.act and len(self.act) > 0:
            output += " " + str(self.act)
        if self.observe and len(self.observe) > 0:
            output += " " + str(self.observe)
        return output
