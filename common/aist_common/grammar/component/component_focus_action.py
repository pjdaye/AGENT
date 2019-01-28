from aist_common.grammar.component.component_action import ComponentAction


class ComponentFocusAction(ComponentAction):
    def __init__(self, capture):
        super().__init__("FOCUS", capture, capture)
        self.variable = capture

    def __str__(self):
        output = "FOCUS {} IN COLLECTION".format(self.variable)
        return output
