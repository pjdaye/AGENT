import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from page_analysis_service.services.concrete_state_featurizer import ConcreteStateFeaturize
from page_analysis_service.services.confusion_matrix import print_cm
from page_analysis_service.services.frame_mapper import FrameMapper
from page_analysis_service.utils.log import get_logger
from page_analysis_service.utils.pickler import ReadWritePickles

RUN_LIVE = True
BASE_PATH = 'page_analysis_service/data'
LOGGER = get_logger('page_analysis_service')
PICKLER = ReadWritePickles()
PICKLER.base_path = BASE_PATH


class PageAnalysisService:
    def __init__(self):
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

        self.__label_classifier_df = pd.read_csv(f'{BASE_PATH}/label_candidates_sys.csv')
        self.__label_classifier_df.replace(self.feature_mapping, inplace=True)
        self.__label_classifier_df_orig = self.__label_classifier_df.copy(deep=True)

        self.__error_msg_classifier_df = pd.read_csv(f'{BASE_PATH}/error_messages_sys.csv')
        self.__error_msg_classifier_df.replace(self.feature_mapping, inplace=True)
        self.__error_msg_classifier_df_orig = self.__error_msg_classifier_df.copy(deep=True)

        self.__commit_classifier_df = pd.read_csv(f'{BASE_PATH}/commits_sys.csv')
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

        LOGGER.info('Processing first')

        for data_point in df_first.values:
            widget_key = data_point[0]
            if data_point[4] == 0.0:
                continue
            data_point = data_point[1:].reshape(1, -1)
            pred = self.__label_classifier.predict(data_point)
            if pred[0] == 1 and widget_key not in self.negativeStorage["labelCandidates"]:
                LOGGER.debug(self.storage)
                data["labelCandidates"].append(widget_key)

        LOGGER.info('Label candidates')

        for labelCandidate in self.storage["labelCandidates"]:
            if labelCandidate not in data["labelCandidates"]:
                data["labelCandidates"].append(labelCandidate)

        LOGGER.info('Reprocessing first')

        for data_point in df_first.values:
            widget_key = data_point[0]
            if data_point[4] == 0.0:
                continue
            data_point = data_point[1:].reshape(1, -1)
            pred = self.__error_msg_classifier.predict(data_point)

            if pred[0] == 1 and widget_key not in data["labelCandidates"] and widget_key not in \
                    self.negativeStorage["errorMessages"]:
                data["errorMessages"].append(widget_key)

            pred = self.__commit_classifier.predict(data_point)
            if pred[0] == 1 and widget_key not in data["labelCandidates"] and widget_key not in \
                    self.negativeStorage["errorMessages"]:
                data["commits"].append(widget_key)

        LOGGER.info('Checking error messages')

        for errorMessage in self.storage["errorMessages"]:
            if errorMessage not in data["errorMessages"]:
                data["errorMessages"].append(errorMessage)

        LOGGER.info('THIRD PROCESSING')

        for data_point in df_sec.values:
            widget_key = data_point[0]
            if data_point[4] == 0.0:
                continue
            data_point = data_point[1:].reshape(1, -1)
            pred = self.__page_title_classifier.predict(data_point)
            if pred[0] == 1 and widget_key not in self.negativeStorage["pageTitles"]:
                data["pageTitles"].append(widget_key)

        LOGGER.info('Processing Titles ')

        for pageTitle in self.storage["pageTitles"]:
            if pageTitle not in data["pageTitles"]:
                data["pageTitles"].append(pageTitle)

        LOGGER.info('Returning data')

        return data

    def add_element(self, element):
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
