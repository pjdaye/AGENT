import pymongo as pm
import pymongo.errors as pme
import datetime

from Pterodactyl.Models.JSONToAbstractState import JSONToAbstractState
from PageAnalysisService.Services.ClusterClassifier.Classifier import Cluster

__author__ = "RobertV"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"


class MongoCheckpointer:
    def __init__(self, cfg):
        self.TTL = cfg.CHECKPOINT_TTL
        self.client = self._connect_to_DB(cfg)

    def close(self):
        self.client.close()

    def _connect_to_DB(self, config):
        client = pm.MongoClient(config.MONGO_HOST)
        db = client[config.MONGO_DB]
        self.collection = db["ClusterCheckpoints"]
        try:
            self.collection.drop_index("createdAt_1")
        except pme.OperationFailure as ex:
            # Ignore if we don't have an index to drop
            pass
        if self.TTL is not None:
            self.collection.create_index([("createdAt", 1)], expireAfterSeconds=self.TTL)
        self.collection.create_index([("version_id", 1)])
        return client

    def save_content(self, version_id, K, content):
        string_cluster_set = {}
        cluster_set = content["cluster_set"]
        for cluster_id in cluster_set:
            cluster = cluster_set[cluster_id]
            cluster_str = str(cluster_id)
            string_cluster_set[cluster_str] = self.cluster_to_JSON(cluster)

        content["cluster_set"] = string_cluster_set
        content["createdAt"] = datetime.datetime.utcnow()
        self.collection.insert(content)

    def get_content(self, version_id, K, tag):
        content = self.collection.find_one({"version_id": version_id, "K" : K, "tag": tag})
        if content is None:
            return None
        cluster_set = {}
        j_cluster_set = content["cluster_set"]
        for cluster_str in j_cluster_set:
            j_cluster = j_cluster_set[cluster_str]
            cluster_id = int(cluster_str)
            cluster_set[cluster_id] = self.cluster_from_JSON(j_cluster)

        content["cluster_set"] = cluster_set
        return content

    def cluster_to_JSON(self, cluster):
        j_doc = {}
        converter = JSONToAbstractState()
        if cluster.center is not None:
            j_center = converter.build_graph_service_request_from_abstract_state(cluster.center)
            self.__vector_to_mongo(j_center)
            j_doc["center"] = j_center

        j_members = []
        for member in cluster.members:
            j_member = converter.build_graph_service_request_from_abstract_state(member)
            self.__vector_to_mongo(j_member)
            j_members.append(j_member)
        j_doc["members"] = j_members
        return j_doc

    def __vector_to_mongo(self, j_state):
        vector = j_state["vector"]
        new_vector = {}
        for vid in vector:
            m_vid = vid.replace(".", "_")
            new_vector[m_vid] = vector[vid]
        j_state["vector"] = new_vector

    def cluster_from_JSON(self, j_cluster):
        cluster = Cluster()
        converter = JSONToAbstractState()
        j_center = j_cluster["center"]
        self.__vector_from_mongo(j_center)
        cluster.center = converter.build_state_from_graph_service_response(j_center)

        members = []
        for j_member in j_cluster["members"]:
            self.__vector_from_mongo(j_member)
            member = converter.build_state_from_graph_service_response(j_member)
            members.append(member)
        cluster.members = members

        return cluster

    def __vector_from_mongo(self, j_state):
        vector = j_state["vector"]
        new_vector = {}
        for vid in vector:
            m_vid = vid.replace("_", ".")
            new_vector[m_vid] = vector[vid]
        j_state["vector"] = new_vector
