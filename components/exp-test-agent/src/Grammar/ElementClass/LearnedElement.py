

class LearnedElement:
    def __init__(self, eq_class):
        self.element_class = eq_class

    def __str__(self):
        return "LEARNED_ELCLASS_" + str(self.element_class)
