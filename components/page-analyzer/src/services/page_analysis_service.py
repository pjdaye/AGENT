"""Handles web-page element classification and training requests."""

import os

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from services.concrete_state_featurizer import ConcreteStateFeaturize
from services.confusion_matrix import print_cm
from services.frame_mapper import FrameMapper

from aist_common.log import get_logger
from aist_common.pickler import ReadWritePickles

RUN_LIVE = True
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
LOGGER = get_logger('page_analysis_service')
PICKLER = ReadWritePickles()


class PageAnalysisService:
    """Handles web-page element classification and training requests."""

    def __init__(self, base_path=None):
        """ Initializes the PageAnalysisService class.

        :param base_path: An optionally provided base path from which to load pickled classifiers from.
        """

        self.__featurize = ConcreteStateFeaturize()
        self.__frame_mapper = FrameMapper()

        self.storage = {
            "labelCandidates": [],
            "errorMessages": [],
            "pageTitles": []
        }
        self.negativeStorage = {
            "labelCandidates": [],
            "errorMessages": [],
            "pageTitles": []
        }

        self.feature_mapping = {
            "Nearest_Color": {
                "black": 0,
                "white": 1,
                "red": 2,
                "blue": 3,
                "grey": 4,
                "yellow": 5,
                "orange": 6,
                "green": 7,
                "purple": 8
            },
            "Nearest_Bg_Color": {
                "black": 0,
                "white": 1,
                "red": 2,
                "blue": 3,
                "grey": 4,
                "yellow": 5,
                "orange": 6,
                "green": 7,
                "purple": 8
            },
            "Class": {
                "None": 0,
                "PageTitle": 1,
                "LabelCandidate": 1,
                "ErrorMessage": 1
            },
        }

        # Test hook.
        if base_path is None:
            base_path = BASE_PATH

        PICKLER.base_path = base_path

        self.__label_classifier_df = pd.read_csv(f'{base_path}/label_candidates_sys.csv')
        self.__label_classifier_df.replace(self.feature_mapping, inplace=True)
        self.__label_classifier_df_orig = self.__label_classifier_df.copy(deep=True)

        self.__error_msg_classifier_df = pd.read_csv(f'{base_path}/error_messages_sys.csv')
        self.__error_msg_classifier_df.replace(self.feature_mapping, inplace=True)
        self.__error_msg_classifier_df_orig = self.__error_msg_classifier_df.copy(deep=True)

        self.__commit_classifier_df = pd.read_csv(f'{base_path}/commits_sys.csv')
        self.__commit_classifier_df.replace(self.feature_mapping, inplace=True)
        self.__commit_classifier_df_orig = self.__commit_classifier_df.copy(deep=True)

        # Load system-delivered classifiers.

        self.__label_classifier = PICKLER.read('label_candidates.clf')

        self.__error_msg_classifier = PICKLER.read('error_messages.clf')

        self.__commit_classifier = PICKLER.read('commits.clf')

        self.__page_title_classifier = PICKLER.read('page_titles.clf')

        # Load live, trainable classifiers.

        self.__label_classifier_live = PICKLER.read('label_candidates_live.clf')

        self.__error_msg_classifier_live = PICKLER.read('error_messages_live.clf')

        self.__commit_classifier_live = PICKLER.read('commits_live.clf')

        if RUN_LIVE:
            self.__label_classifier = self.__label_classifier_live
            self.__error_msg_classifier = self.__error_msg_classifier_live
            self.__commit_classifier = self.__commit_classifier_live

    def get_page_titles(self, concrete_state):
        """ Run page title classifier for the provided concrete state.

        :param concrete_state: The input concrete state.

        :return: A page analysis containing keys for elements that were classified as page titles.
        """

        data = {
            "pageTitles": []
        }

        df = self.__featurize.convert_to_feature_frame(concrete_state, measure_color_distance=False)
        df = self.__frame_mapper.map_page_titles(df)

        for data_point in df.values:
            widget_key = data_point[0]
            if data_point[4] == 0.0:
                continue
            data_point = data_point[1:].reshape(1, -1)
            pred = self.__page_title_classifier.predict(data_point)
            if pred[0] == 1:
                data["pageTitles"].append(widget_key)

        return data

    def get_page_analysis(self, concrete_state):
        """ Run all element classifiers for the provided concrete state.

        :param concrete_state: The input concrete state.

        :return: A page analysis containing keys for elements that were classified.
        """

        data = {
            "pageTitles": [],
            "labelCandidates": [],
            "errorMessages": [],
            "commits": [],
            "cancels": []
        }

        LOGGER.info('Setting up dataframes')

        df = self.__featurize.convert_to_feature_frame(concrete_state)
        df_first = self.__frame_mapper.map_label_candidates(df)
        df_sec = self.__frame_mapper.map_page_titles(df)

        LOGGER.info('Classifying label candidates.')

        for data_point in df_first.values:
            widget_key = data_point[0]
            if data_point[4] == 0.0:
                continue
            data_point = data_point[1:].reshape(1, -1)
            pred = self.__label_classifier.predict(data_point)
            if pred[0] == 1:
                data["labelCandidates"].append(widget_key)

        LOGGER.info('Classifying other elements.')

        for data_point in df_first.values:
            widget_key = data_point[0]
            if data_point[4] == 0.0:
                continue
            data_point = data_point[1:].reshape(1, -1)
            pred = self.__error_msg_classifier.predict(data_point)

            if pred[0] == 1 and widget_key not in data["labelCandidates"]:
                data["errorMessages"].append(widget_key)

            pred = self.__commit_classifier.predict(data_point)
            if pred[0] == 1 and widget_key not in data["labelCandidates"]:
                data["commits"].append(widget_key)

        for data_point in df_sec.values:
            widget_key = data_point[0]
            if data_point[4] == 0.0:
                continue
            data_point = data_point[1:].reshape(1, -1)
            pred = self.__page_title_classifier.predict(data_point)
            if pred[0] == 1:
                data["pageTitles"].append(widget_key)

        LOGGER.info('Returning classifications.')

        return data

    def add_element(self, element):
        """ Adds a labeled element to the underlying training data, and retrains the underlying classifiers.

        :param element: The element payload (must also contain the associated concrete state).
        """

        target_widget_key = element['id']

        concrete_state = element['state']

        element_class = element['classes'][0]

        df = self.__featurize.convert_to_feature_frame(concrete_state)

        df_first = self.__frame_mapper.map_label_candidates(df)

        df_in_use = self.__label_classifier_df

        if element_class == 'errorMessage':
            df_in_use = self.__error_msg_classifier_df
        elif element_class == 'commit':
            df_in_use = self.__commit_classifier_df

        for data_point in df_first.values:
            widget_key = data_point[0]
            if widget_key == target_widget_key:
                df_row = df_first[df_first['Key'] == widget_key]
                df_row['Class'] = 1
                df_row = df_row.drop(['Key'], axis=1)
                df_row.reset_index(drop=True, inplace=True)
                df_in_use = pd.concat([df_in_use, df_row], ignore_index=True)

        features = df_in_use.columns[:-1]
        train_true_y = df_in_use['Class']
        train_true_y = train_true_y.astype('int')

        clf = RandomForestClassifier(n_estimators=100)

        clf.fit(df_in_use[features], train_true_y)

        if element_class == 'errorMessage':
            self.__error_msg_classifier = clf
            self.__error_msg_classifier_df = df_in_use

            PICKLER.write('error_messages_live.clf', clf)

        elif element_class == 'labelCandidate':
            self.__label_classifier = clf
            self.__label_classifier_df = df_in_use

            PICKLER.write('label_candidates_live.clf', clf)

        elif element_class == 'commit':
            self.__commit_classifier = clf
            self.__commit_classifier_df = df_in_use

            PICKLER.write('commits_live.clf', clf)

        train_pred_y = clf.predict(df_in_use[features])

        small_train_true_y = []
        small_train_pred_y = []

        target_names = ['None', 'Match']

        for i in range(len(train_true_y)):
            example = train_true_y[i]
            if target_names[example] == "None":
                continue
            small_train_true_y.append(train_true_y[i])
            small_train_pred_y.append(train_pred_y[i])

        LOGGER.info("")
        LOGGER.info("Metrics (vs. training set)")
        LOGGER.info("Accuracy (all): " + str(accuracy_score(train_true_y, train_pred_y)))
        LOGGER.info("Accuracy (excluding Nones): " + str(accuracy_score(small_train_true_y, small_train_pred_y)))
        LOGGER.info("")
        LOGGER.info(classification_report(train_true_y, train_pred_y, target_names=target_names))

        train_true_y = [target_names[j] for j in train_true_y]
        train_pred_y = [target_names[j] for j in train_pred_y]
        cm = confusion_matrix(train_true_y, train_pred_y, labels=target_names)
        print_cm(cm, target_names)

        LOGGER.info("Done training")
        LOGGER.info(self.storage)
