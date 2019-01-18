

class ActionableState:

    def __init__(self):
        self.widget_map = {}
        self.widgets = []
        self.static_widgets = []
        self.hash = 0

    def add_widget(self, widget):
        self.widget_map[widget["key"]] = widget
        self.widgets.append(widget)

    def add_static_widget(self, widget):
        self.static_widgets.append(widget)

    def find_widget_with_label(self, label, action):
        for widget in self.widgets:
            if widget['label'] and widget['label'].replace(' ', '').upper() == label:
                if action in widget['actions']:
                    return widget
        return None

    def calculate_hash(self):
        to_hash = (w["key"] for w in self.widgets)
        self.hash = hash(frozenset(to_hash))
