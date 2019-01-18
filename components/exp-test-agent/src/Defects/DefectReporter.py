from Defects.Defect import Defect


class DefectReporter:
    def __init__(self):
        self.defects = []

    def add_defect(self, flow, flow_actions, failure_index):
        self.defects.append(Defect(flow, flow_actions, failure_index))

    def report_defects(self):
        pass
