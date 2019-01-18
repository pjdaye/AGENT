

class Component:
    def __init__(self, element_class, ident):
        self.element_class = element_class
        self.ident = ident

    def __str__(self):
        output = ""
        if self.element_class:
            output += "{}".format(str(self.element_class))
        if self.element_class and self.ident:
            output += " {}".format(self.ident)
        elif self.ident:
            output += "{}".format(self.ident)
        return output
