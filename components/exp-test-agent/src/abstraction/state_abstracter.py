"""Converts a concrete state into an abstract state representation in order to control state explosion."""
from abstraction.actionable_state import ActionableState


class StateAbstracter:
    """Converts a concrete state into an abstract state representation in order to control state explosion."""

    ACTIONABLE_TAGS = ['A', 'INPUT', 'BUTTON']

    def process(self, concrete_state):
        """ Converts a concrete state into an abstract state.

        :param concrete_state: The concrete state scraped from the SUT.

        :return: The abstract state.
        """

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
        """ Attempts to build a unique CSS or jQuery selector for a given widget.

        :param widget: The widget for which to build a selector.
        :param selectors: All of the selectors that have already been built for the same abstract state.

        :return: A CSS or jQuery selector.
        """

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
            selector += ":visible:eq({})".format(current_index+1)
        else:
            selectors[selector] = 0
            selector += ":visible:eq(0)"
        return selector

    @staticmethod
    def get_actions(widget):
        """ Returns the possible actions given a widget.

        :param widget: The widget.

        :return: A list of possible actions.
        """

        actions = []
        tag = widget["properties"]["tagName"]
        if tag == 'A':
            actions.append('click')
        elif tag == 'INPUT':
            actions.append('set')
        elif tag == 'BUTTON':
            actions.append('click')
        return actions
