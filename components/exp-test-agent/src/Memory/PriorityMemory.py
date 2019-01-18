import random


class PriorityMemory:

    PRIORITY = ['INPUT', 'BUTTON']

    def __init__(self):
        self.memory = {}

    def choose_widget(self, act_state):
        memory_cells = self.memory[act_state.hash]

        for widget in act_state.widgets:
            widget_key = widget["key"]
            if widget_key not in memory_cells.keys():
                memory_cells[widget_key] = 0

        highest_cell = -1

        cell_map = self.memory[act_state.hash]
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
                widget_tag = act_state.widget_map[widget_key]["properties"]["tagName"]
                if widget_tag in PriorityMemory.PRIORITY:
                    priority_cells.append(widget_key)

        if len(priority_cells) > 0:
            chosen_widget = random.choice(priority_cells)
        else:
            chosen_widget = random.choice(low_cells)

        chosen_widget = act_state.widget_map[chosen_widget]

        return chosen_widget

    def update_memory(self, act_state, chosen_widget):
        if act_state.hash in self.memory:
            if chosen_widget["key"] in self.memory[act_state.hash]:
                memory_cell = self.memory[act_state.hash][chosen_widget["key"]]
                self.memory[act_state.hash][chosen_widget["key"]] = memory_cell + 1
            else:
                self.memory[act_state.hash][chosen_widget["key"]] = 1
        else:
            self.memory[act_state.hash] = {}
            self.memory[act_state.hash][chosen_widget["key"]] = 1

    def in_memory(self, hash):
        return hash in self.memory

    @staticmethod
    def choose_randomly(act_state):
        priority_cells = []
        all_cells = []
        for widget in act_state.widgets:
            all_cells.append(widget)
            widget_tag = widget["properties"]["tagName"]
            if widget_tag in PriorityMemory.PRIORITY:
                priority_cells.append(widget)
        if len(priority_cells) > 0:
            return random.choice(priority_cells)
        return random.choice(all_cells)


