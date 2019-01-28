

class ComponentAction:
    def __init__(self, action, eq_class, component):
        self.action = action
        self.equivalence_class = eq_class
        self.component = component

    def __str__(self):
        output = "{} {}".format(self.action, self.equivalence_class)
        if self.component:
            output += " " + str(self.component)
        return output
