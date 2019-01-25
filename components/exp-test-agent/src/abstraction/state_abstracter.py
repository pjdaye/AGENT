from abstraction.actionable_state import ActionableState


class StateAbstracter:

    ACTIONABLE_TAGS = ['A', 'INPUT', 'BUTTON']

    def __init__(self):
        pass

    def process(self, concrete_state):
        act_state = ActionableState()
        selectors = {}
        for key, widget in concrete_state["widgets"].items():
            tag = widget["properties"]["tagName"]
            if tag in StateAbstracter.ACTIONABLE_TAGS:
                selector = self.build_selector(widget, selectors)
                widget["selector"] = selector

                actions = self.get_actions(widget)
                widget["actions"] = actions

                if len(actions) > 0:
                    act_state.add_widget(widget)
            else:
                act_state.add_static_widget(widget)
            act_state.calculate_hash()
        return act_state

    @staticmethod
    def build_selector(widget, selectors):
        tag = widget["properties"]["tagName"]
        widget_id = widget["properties"]["id"] if "id" in widget["properties"] else None
        href = widget["properties"]["href"] if "href" in widget["properties"] else None
        selector = tag

        if widget_id:
            selector += "[id='{}']".format(widget_id)
        if href:
            selector += "[href='{}']".format(href)

        if selector in selectors:
            current_index = selectors[selector]
            selectors[selector] = selectors[selector] + 1
            selector += ":eq({})".format(current_index+1)
        else:
            selectors[selector] = 0
            selector += ":eq(0)"
        return selector

    @staticmethod
    def get_actions(widget):
        actions = []
        tag = widget["properties"]["tagName"]
        if tag == 'A':
            actions.append('click')
        elif tag == 'INPUT':
            actions.append('set')
        elif tag == 'BUTTON':
            actions.append('click')
        return actions
