from PteroTF.Visualizers.DataVisualizer import DataVisualizer

__author__ = "RobertV"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"


class DistanceVisualizer:
    def __init__(self, data):
        self.state_lookup = {}
        for state in data:
            self.state_lookup[state.hash] = state

    def show_distances(self, classifier):
        people_hash = 9077472515444840285
        signout_hash = -3458861185337882842

        s1 = self.state_lookup[people_hash]
        s2 = self.state_lookup[signout_hash]
        d = classifier.distance(s1, s2)
        print(d)


class ScreenShotVisualizer:
    def __init__(self, cluster):
        self.cluster_center = cluster.center
        self.cluster_members = cluster.members

    def __add_to_names(self, names, new_name):
        if new_name not in names:
            names.append(new_name)
        return names

    def __get_index(self, names, name):
        return names.index(name)

    def show_screenshots(self, data_provider):
        sc = data_provider.get_screenshot(self.cluster_center.hash)
        visualizer = DataVisualizer()
        # names = [self.cluster_center.title]
        # examples = [sc]
        # labels = [0]
        # visualizer.show_some_examples(names, examples, labels)

        names = []
        examples = []
        labels = []
        for state in self.cluster_members:
            sc = data_provider.get_screenshot(state.hash)
            examples.append(sc)
            names = self.__add_to_names(names, state.title)
            labels.append(self.__get_index(names, state.title))

        visualizer.show_some_examples(names, examples, labels)

    def compare_screenshots(self, data_provider, s1_hash, s2_hash):
        s1 = self.__get_state_from_hash(s1_hash)
        s2 = self.__get_state_from_hash(s2_hash)

        visualizer = DataVisualizer()
        names = []
        examples = []
        labels = []
        for state in [s1, s2]:
            sc = data_provider.get_screenshot(state.hash)
            examples.append(sc)
            names = self.__add_to_names(names, state.title)
            labels.append(self.__get_index(names, state.title))

        visualizer.show_some_examples(names, examples, labels)

    def __get_state_from_hash(self, state_hash):
        for s in self.cluster_members:
            if s.hash == state_hash:
                return s
        return None
