import os

from pathlib import Path
import pickle

import numpy as np
import base64
import io

# TODO: Need to include matplotlib in Dockerfile.
# import matplotlib.image as mpimg

from Pterodactyl.Common.EurekaConnection.EurekaSession import EurekaSession
from Pterodactyl.GraphServiceAPI.GraphServiceClient import get_graph_service_client

__author__ = "RobertV"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"


class GraphServiceStateProvider:
    def __init__(self, logger, cfg, version_id, eureka_session):
        self.logger = logger
        self.cfg = cfg
        self.version_id = version_id
        self.eureka_session = eureka_session
        self.graph_service_client = None
        self.graph_id = None

    def get_states(self):
        if self.graph_service_client is None:
            self.__set_graph_from_version(self.version_id)
        if self.graph_id is not None:
            states = self.graph_service_client.get_sparse_abstract_states(
                self.graph_id)
        else:
            states = []
        return states

    def get_screenshot(self, state_hash):
        if self.graph_service_client is None:
            self.__set_graph_from_version(self.version_id)
        summary = self.graph_service_client.get_abstract_state_summary(
            self.graph_id, state_hash)
        screenshot = summary.screenshot
        return screenshot

    def __set_graph_from_version(self, version_id):
        self.graph_service_client = get_graph_service_client(
            self.cfg, self.eureka_session)
        version_graph = self.graph_service_client.get_graph_by_version_id(
            version_id)
        if version_graph is not None:
            self.graph_id = version_graph["id"]


class FileCachedStateProvider:
    def __init__(self, graph_service_state_provider, state_data_file_dir):
        self.graph_state_provider = graph_service_state_provider
        version_id = self.graph_state_provider.version_id
        file_name = version_id + ".p"
        self.state_data_file = os.path.join(state_data_file_dir, file_name)

    def get_states(self):
        if self.__local_data_available():
            states = self.__get_local_data()
        else:
            states = self.graph_state_provider.get_states()
            self.__save_data_local(states)
        return states

    def get_screenshot(self, state_hash):
        return self.graph_state_provider.get_screenshot(state_hash)

    def __local_data_available(self):
        if self.state_data_file is not None and Path(self.state_data_file).is_file():
            return True
        else:
            return False

    def __get_local_data(self):
        with open(self.state_data_file, 'rb') as fo:
            states = pickle.load(fo, encoding='latin1')
        return states

    def __save_data_local(self, data):
        pickle.dump(data, open(self.state_data_file, "wb"))


class StateDataProvider:
    def __init__(self, logger, cfg, eureka_session, version_id):
        self.cfg = cfg
        self.version_id = version_id
        self.provider = None

        self.provider = GraphServiceStateProvider(
            logger, cfg, version_id, eureka_session)
        if hasattr(self.cfg, "STATE_DATA_FILE_DIR"):
            self.provider = FileCachedStateProvider(
                self.provider, self.cfg.STATE_DATA_FILE_DIR)

        self.prescaled_image_shape = (1927, 1264)

    def read_data(self, N=-1):
        states = self.provider.get_states()
        if N > 0 and len(states) >= N:
            return states[:N]
        else:
            return states

    def get_screenshot(self, state_hash):
        screen_shot = self.provider.get_screenshot(state_hash)
        i = base64.b64decode(screen_shot)
        i = io.BytesIO(i)
        # TODO: Need to include matplotlib in Dockerfile.
        # image = mpimg.imread(i)
        # screen_data = self.__clean_image_data(image)
        # return screen_data
        return None

    def __clean_image_data(self, image):
        # shape should be 1927 x 1264 x 4
        if image.shape[0] < self.prescaled_image_shape[0]:
            # pad data
            pad = np.zeros(
                (self.prescaled_image_shape[0] - image.shape[0], image.shape[1], image.shape[2]))
            image = np.vstack((image, pad))
        elif image.shape[0] > self.prescaled_image_shape[0]:
            # trim data
            image = image[:self.prescaled_image_shape[0], :]

        if image.shape[1] < self.prescaled_image_shape[1]:
            # pad data
            pad = np.zeros(
                (image.shape[0], self.prescaled_image_shape[1] - image.shape[1], image.shape[2]))
            image = np.hstack((image, pad))
        elif image.shape[1] > self.prescaled_image_shape[1]:
            # trim data
            image = image[:, :self.prescaled_image_shape[1]]

        assert image.shape[0] == self.prescaled_image_shape[0]
        assert image.shape[1] == self.prescaled_image_shape[1]
        assert image.shape[2] == 4

        r, g, b, a = np.rollaxis(image, axis=-1)
        image = np.dstack([r, g, b])
        return image
