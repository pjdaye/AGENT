import os
import hashlib

from pathlib import Path
import pickle

from PageAnalysisService.Services.ClusterClassifier.MongoCheckpointer import MongoCheckpointer

__author__ = "RobertV"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"


class FileCheckpointer:
    def __init__(self, cfg, checkpoint_dir):
        self.checkpoint_dir = checkpoint_dir

    def save_content(self, version_id, K, content):
        file = self.__make_filename(version_id, K)
        pickle.dump(content, open(file, "wb"))

    def get_content(self, version_id, K, tag):
        file = self.__make_filename(version_id, K)
        if Path(file).is_file():
            with open(file, 'rb') as fo:
                content = pickle.load(fo, encoding='latin1')
        else:
            content = None
        return content

    def __make_filename(self, version_id, K):
        file_name = "{}_{}.p".format(version_id, K)
        checkpoint_file = os.path.join(self.checkpoint_dir, file_name)
        return checkpoint_file


class Checkpointer:
    def __init__(self, cfg, version_id, K, state_data):
        self.cfg = cfg
        self.version_id = version_id
        self.K = K
        self.data_hash = self.__data_hash(state_data)
        if hasattr(cfg, "CHECKPOINT_DIR"):
            self.checkpoint_engine = FileCheckpointer(cfg, cfg.CHECKPOINT_DIR)
        else:
            self.checkpoint_engine = MongoCheckpointer(cfg)

    def save_checkpoint(self, cluster_set):
        content = self.__make_checkpoint_content(cluster_set)
        self.checkpoint_engine.save_content(self.version_id, self.K, content)

    def get_checkpoint(self):
        content = self.checkpoint_engine.get_content(self.version_id, self.K, self.data_hash)
        if content is not None:
            cluster_set = content["cluster_set"]
            content_hash = content["tag"]
            if content_hash != self.data_hash:
                raise Exception("Content hash does not match.  States have changed")
        else:
            cluster_set = None
        return cluster_set

    def __make_checkpoint_content(self, cluster_set):
        content = {}
        content["version_id"] = self.version_id
        content["K"] = self.K
        content["tag"] = self.data_hash
        content["cluster_set"] = cluster_set
        return content

    def __data_hash(self, state_data):
        hash_items = []
        for state in state_data:
            hash_items.append(state.hash)
        sorted(hash_items)
        hash_tuple = tuple(hash_items)
        return hash(hash_tuple)
