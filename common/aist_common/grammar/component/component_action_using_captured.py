from aist_common.grammar.component.component_action import ComponentAction


class ComponentActionUsingCaptured(ComponentAction):
    def __init__(self, captured, component):
        super().__init__(captured, captured, component)
        self.variable = captured

    def __str__(self):
        output = "TRY {} {}".format(self.variable, self.component)
        return output
