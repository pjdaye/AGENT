"""Represents an SUT state, and contains a list of both actionable and non-actionable widgets."""


class ActionableState:
    """Represents an SUT state, and contains a list of both actionable and non-actionable widgets."""

    def __init__(self):
        """ Initializes the ActionableState class.
        """

        self.widget_map = {}
        self.widgets = []
        self.static_widgets = []
        self.hash = 0

    def add_widget(self, widget):
        """Adds a widget to the state.

        :param widget: The widget to add.
        """

        self.widget_map[widget["key"]] = widget
        self.widgets.append(widget)

    def add_static_widget(self, widget):
        """Adds a widget that is not actionable to the state.

        :param widget: The widget to add.
        """

        self.static_widgets.append(widget)

    def find_widget_with_label(self, label, action):
        """Locates a widget with the requested label and action in the state.

        :param label: The label to include as part of the search.
        :param action: The action to include as part of the search.

        :return: The widget, if found.
        """

        for widget in self.widgets:
            if widget['label'] and widget['label'].replace(' ', '').upper() == label:
                if action in widget['actions']:
                    return widget
        return None

    def calculate_hash(self):
        """ Calculates a hash for the state that is comprised of all actionable widget keys.
        """

        to_hash = (w["key"] for w in self.widgets)
        self.hash = hash(frozenset(to_hash))
