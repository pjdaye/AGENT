"""Extracts labels for each actionable widget in an abstract state."""

import math


class LabelExtraction:
    """Extracts labels for each actionable widget in an abstract state."""

    @staticmethod
    def extract_labels(abstract_state, page_analysis):
        """ Extracts labels for each actionable widget in the given abstract state.
            Relies on element classifications present in the provided page analysis to determine label candidates.

        :param abstract_state: The abstract state to process.
        :param page_analysis: The page analysis output for the provided abstract state (element classifications).
        """

        label_candidates = page_analysis['analysis']['labelCandidates']
        for widget in abstract_state.widgets:
            best_label = None
            best_label_key = None
            best_distance = 99999
            widget_x = widget["properties"]["x"]
            widget_y = widget["properties"]["y"]
            for static_widget in abstract_state.static_widgets:
                should_skip = LabelExtraction._should_skip(static_widget)
                if should_skip:
                    continue
                if static_widget['key'] not in label_candidates:
                    continue
                text = static_widget["properties"]["text"] if "text" in static_widget["properties"] else None
                if text:
                    text_x = static_widget["properties"]["x"]
                    text_y = static_widget["properties"]["y"]
                    new_distance = math.hypot(text_x - widget_x, text_y - widget_y)
                    if new_distance < best_distance:
                        best_distance = new_distance
                        best_label = text
                        best_label_key = static_widget["key"]

            if best_label:
                best_label = best_label.strip()
            widget["label"] = best_label
            widget["label_key"] = best_label_key

    @staticmethod
    def _should_skip(widget):
        """ Determines whether a widget should be skipped when determining if it is a label.
            Generally, we want to skip headers, and other form fields to prevent other fields being assigned as labels.

        :param widget: A widget on an abstract state.
        :return: True if the widget should be skipped.
        """

        tag = widget["properties"]["tagName"]
        if tag in ['BUTTON', 'INPUT', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6']:
            return True
        return False
