""" Combines information from page classifiers along with an abstract test
    flow to generate possible concrete test flows for the SUT."""

import itertools

from flow_execution.concrete_test_flow import ConcreteTestFlow

from aist_common.log import get_logger

LOGGER = get_logger('flow-planner')


class FlowPlanner:
    """ Combines information from page classifiers along with an abstract test
        flow to generate possible concrete test flows for the SUT."""

    def __init__(self):
        """ Initializes the FlowPlanner class.
        """

        self._klass = __class__.__name__

    @staticmethod
    def plan(abstract_state, page_analysis, abstract_flow):
        """ Given an abstract test flow and widget classifications, produces a list of
            possibly executable concrete test flows.

        :param abstract_state: The current abstract state (where a concrete test flow execution would begin from).
        :param page_analysis: The page analysis output for the current abstract state (element classifications).
        :param abstract_flow: The abstract test flow to process.
         
        :return: A list of concrete test flows.
        """

        planned_flows = []

        plan_steps = []

        for action in abstract_flow.act.actions:
            if action.action == 'TRY':
                widget = abstract_state.find_widget_with_label(action.component.ident, 'set')

                if not widget:
                    LOGGER.error("Unable to bind flow act step: " + str(action))
                    return False

                plan_steps.append([(action, widget)])

            elif action.action == 'CLICK':
                element_class = action.equivalence_class.element_class

                if element_class is None and action.equivalence_class.ident is not None:
                    element_class = action.equivalence_class.ident

                if element_class not in page_analysis['analysis']:
                    LOGGER.error("Unable to bind flow act step: " + str(action))
                    return False

                candidate_widgets = page_analysis['analysis'][element_class]

                possible_steps = []

                for candidate_widget_key in candidate_widgets:
                    if candidate_widget_key not in abstract_state.widget_map or \
                            'click' not in abstract_state.widget_map[candidate_widget_key]['actions']:
                        continue

                    actual_widget = abstract_state.widget_map[candidate_widget_key]

                    possible_steps.append((action, actual_widget))

                plan_steps.append(possible_steps)

        cartesian_product = itertools.product(*plan_steps)

        for seq in cartesian_product:
            planned_flows.append(ConcreteTestFlow(None, abstract_state, abstract_flow, seq))

        return planned_flows
