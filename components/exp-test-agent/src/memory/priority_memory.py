"""Keeps track of which widgets have been interacted with for every abstract state."""

import random


class PriorityMemory:
    """Keeps track of which widgets have been interacted with for every abstract state."""

    PRIORITY = ['INPUT', 'BUTTON']

    def __init__(self):
        """ Initializes the PriorityMemory class.
        """

        self.memory = {}

    def choose_widget(self, abstract_state):
        """ Chooses a widget to interact with from the given abstract state.
            Prefers to interact with a widget that has not yet been interacted with within the running session.
            Prioritizes element tags defined in the PriorityMemory.PRIORITY list.
            Given an interaction count tie across multiple widgets, randomly chooses a widget to interact with.

        :param abstract_state: The abstract state to choose a widget from.

        :return: The chosen widget.
        """

        memory_cells = self.memory[abstract_state.hash]

        for widget in abstract_state.widgets:
            widget_key = widget["key"]
            if widget_key not in memory_cells.keys():
                memory_cells[widget_key] = 0

        highest_cell = -1

        cell_map = self.memory[abstract_state.hash]
        for cell_value in cell_map.values():
            if cell_value > highest_cell:
                highest_cell = cell_value

        lowest_cell = highest_cell
        for cell_value in cell_map.values():
            if cell_value < lowest_cell:
                lowest_cell = cell_value

        priority_cells = []
        low_cells = []
        for widget_key, cell_value in cell_map.items():
            if cell_value == lowest_cell:
                low_cells.append(widget_key)
                widget_tag = abstract_state.widget_map[widget_key]["properties"]["tagName"]
                if widget_tag in PriorityMemory.PRIORITY:
                    priority_cells.append(widget_key)

        if len(priority_cells) > 0:
            chosen_widget = random.choice(priority_cells)
        else:
            chosen_widget = random.choice(low_cells)

        chosen_widget = abstract_state.widget_map[chosen_widget]

        return chosen_widget

    def update_memory(self, abstract_state, chosen_widget):
        """ Updates internal memory, updating the interaction count for the provided chosen widget.

        :param abstract_state: The abstract state for which we are updating our internal memory on.
        :param chosen_widget: The widget to increase the interaction count on.
        """

        if abstract_state.hash in self.memory:
            if chosen_widget["key"] in self.memory[abstract_state.hash]:
                memory_cell = self.memory[abstract_state.hash][chosen_widget["key"]]
                self.memory[abstract_state.hash][chosen_widget["key"]] = memory_cell + 1
            else:
                self.memory[abstract_state.hash][chosen_widget["key"]] = 1
        else:
            self.memory[abstract_state.hash] = {}
            self.memory[abstract_state.hash][chosen_widget["key"]] = 1

    def in_memory(self, abstract_state_hash):
        """ Checks whether the provided abstract state hash is in the memory.

        :param abstract_state_hash: The abstract state hash.

        :return: True if the hash is in memory.
        """

        return abstract_state_hash in self.memory

    @staticmethod
    def choose_randomly(abstract_state):
        """ Randomly chooses a widget (taking tag priority into account) from an abstrat state.

        :param abstract_state: The abstract state to choose a widget from.

        :return: The chosen widget.
        """

        priority_cells = []
        all_cells = []
        for widget in abstract_state.widgets:
            all_cells.append(widget)
            widget_tag = widget["properties"]["tagName"]
            if widget_tag in PriorityMemory.PRIORITY:
                priority_cells.append(widget)
        if len(priority_cells) > 0:
            return random.choice(priority_cells)
        return random.choice(all_cells)
