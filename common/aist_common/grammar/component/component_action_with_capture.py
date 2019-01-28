from aist_common.grammar.component.component_action import ComponentAction


class ComponentActionWithCapture(ComponentAction):
    def __init__(self, action, eq_class, component, variable):
        super().__init__(action, eq_class, component)
        self.variable = variable

    def __str__(self):
        output = "{} {}".format(super().__str__(), self.variable)
        return output
