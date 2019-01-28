

class Observation:
    def __init__(self):
        self.observe = True
        self.qualifier_list = None
        self.component = None

    def positive(self):
        self.observe = True
        return self

    def negative(self):
        self.observe = False
        return self

    def with_qualifiers(self, qualifier_list):
        self.qualifier_list = qualifier_list
        return self

    def with_component(self, component):
        self.component = component
        return self

    def __str__(self):
        output = "OBSERVE" if self.observe else "NOTOBSERVE"
        if self.qualifier_list and len(self.qualifier_list) > 0:
            output += " " + str(self.qualifier_list)
        if self.component:
            output += " " + str(self.component)
        return output
