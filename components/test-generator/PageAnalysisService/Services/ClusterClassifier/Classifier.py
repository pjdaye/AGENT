import random
import sys
import numpy as np
import time

from PageAnalysisService.Services.ClusterClassifier.utils import cosine_similarity

__author__ = "RobertV"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"


class Cluster:
    def __init__(self):
        self.center = None
        self.members = []


class ClusterStateClassifier:
    def __init__(self, logger, cfg, K, checkpointer):
        self.logger = logger
        self.cfg = cfg
        self.K = K
        self.clusters = {}
        self.d_count = 0
        self.max_loops = cfg.MAX_ITERATIONS
        self.klass = "ClusterStateClassifier"
        self.cp = checkpointer

    def distance(self, s1, s2):
        cos = cosine_similarity(s1.vector, s2.vector)
        distance = 1.0 - cos
        self.d_count += 1
        return distance

    def get_clusters(self, context, states):
        self.clusters = self.cp.get_checkpoint()
        if self.clusters is None:
            self.__find_best_clusters(context, states)
            self.cp.save_checkpoint(self.clusters)

    def __find_best_clusters(self, context, states):
        self.logger.Info(context, self.klass, "__find_best_clusters",
                         "Start Looping at {}".format(time.ctime()))
        self.__set_random_cluster_centers(states)
        diffs = 1
        loop = 0

        while diffs > 0 and loop < self.max_loops:
            self.d_count = 0
            start = time.time()
            self.__assign_states_to_clusters(states)
            end = time.time()
            self.logger.Info(context, self.klass, "__find_best_clusters",
                             "Assign States took {:0.0F} mSec., {} distance calculations".format(
                                            1000 * (end-start), self.d_count))

            self.d_count = 0
            start = time.time()
            diffs = self.__find_center_of_clusters()
            end = time.time()
            self.logger.Info(context, self.klass, "__find_best_clusters",
                             "Find Centers took {:0.0f} mSec., {} distance calculations".format(
                                            1000 * (end-start), self.d_count))
            loop += 1
            self.show_progress(diffs, loop)

    def __set_random_cluster_centers(self, states):
        if len(states) < self.K:
            self.K = len(states)
        random_indexes = random.sample(range(len(states)), self.K)
        clusters = {}
        for idx in random_indexes:
            cluster = Cluster()
            cluster.center = states[idx]
            cluster.members = []
            clusters[cluster.center.hash] = cluster
        self.clusters = clusters

    def __assign_states_to_clusters(self, states):
        for cluster_hash in self.clusters:
            cluster = self.clusters[cluster_hash]
            cluster.members = []

        for state in states:
            min_distance = sys.float_info.max
            best_cluster = None

            for cluster_hash in self.clusters:
                cluster = self.clusters[cluster_hash]
                center = cluster.center
                distance = self.distance(state, center)
                if distance < min_distance:
                    min_distance = distance
                    best_cluster = cluster

            best_cluster.members.append(state)

    def __find_center_of_clusters(self):
        num_diffs = 0
        for cluster_hash in self.clusters:
            cluster = self.clusters[cluster_hash]
            min_sum_of_distance = sys.float_info.max
            best_center = None

            # Define the center to be the point with the minimum sum of distances to all other points
            # Similar to k_mediod (see https://en.wikipedia.org/wiki/K-medoids)

            # First calculate all inter-state distances
            num_members = len(cluster.members)

            # cache distances since they are expensive to calculate.
            distances = np.full((num_members, num_members), -1)
            for idx1 in range(num_members):
                s1 = cluster.members[idx1]
                sum_of_distance = 0.0
                for idx2 in range(num_members):
                    s2 = cluster.members[idx2]
                    distance = distances[idx1][idx2]
                    if distance < 0.0:
                        distance = self.distance(s1, s2)
                        distances[idx1][idx2] = distance
                        distances[idx2][idx1] = distance

                    sum_of_distance += distance

                if sum_of_distance < min_sum_of_distance:
                    min_sum_of_distance = sum_of_distance
                    best_center = s1

            if best_center is None:
                # This cluster has no members
                best_center = cluster.center

            if best_center.hash != cluster.center.hash:
                num_diffs += 1
            cluster.center = best_center

        # Rebuild cluster hash
        new_clusters = {}
        for ch in self.clusters:
            cluster = self.clusters[ch]
            new_clusters[cluster.center.hash] = cluster

        self.clusters = new_clusters
        return num_diffs

    # info helpers
    def show_progress(self, diffs, loop):
        self.__show_low_details("Looped {} times, now there are {} diffs at {}".format(loop, diffs, time.ctime()))
        for cluster_hash in self.clusters:
            cluster = self.clusters[cluster_hash]
            center = cluster.center.title
            count = len(cluster.members)
            self.__show_high_details("----Cluster center <{}> has {} members".format(center, count))

    def show_stats(self):
        self.__show_developer("\n\n--Cluster Results ----")
        for cluster_hash in self.clusters:
            cluster = self.clusters[cluster_hash]
            center = cluster.center.title
            hash_v = cluster.center.hash
            self.__show_developer("----Cluster <{}> ({})----".format(center, hash_v))
            for member_state in cluster.members:
                member = member_state.title
                hash_v = member_state.hash
                self.__show_developer("        + <{}> ({})".format(member, hash_v))

    def __show_developer(self, msg):
        print(msg)
        pass

    def __show_low_details(self, msg):
        # print(msg)
        pass

    def __show_high_details(self, msg):
        # print(msg)
        pass
