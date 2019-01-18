#!/usr/bin/env python

import json

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from PageAnalysisService.Services.ConfusionMatrix import print_cm, insert_row

__author__ = "DionnyS"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"

import pickle
import numpy as np
import pandas as pd

from PageAnalysisService.Services.ConcreteStateFeaturize import ConcreteStateFeaturize
from PageAnalysisService.Services.FrameMapper import FrameMapper

RUN_LIVE = True


class PageAnalysisService:
    def __init__(self, acl):
        self.__acl = acl
        self.__featurize = ConcreteStateFeaturize()
        self.__frame_mapper = FrameMapper()

        print("INIT")

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

        self.__label_classifier_df = pd.read_csv('label_candidates_sys.csv')
        self.__label_classifier_df.replace(self.feature_mapping, inplace=True)
        self.__label_classifier_df_orig = self.__label_classifier_df.copy(deep=True)

        self.__error_msg_classifier_df = pd.read_csv('error_messages_sys.csv')
        self.__error_msg_classifier_df.replace(self.feature_mapping, inplace=True)
        self.__error_msg_classifier_df_orig = self.__error_msg_classifier_df.copy(deep=True)

        self.__commit_classifier_df = pd.read_csv('commits_sys.csv')
        self.__commit_classifier_df.replace(self.feature_mapping, inplace=True)
        self.__commit_classifier_df_orig = self.__commit_classifier_df.copy(deep=True)

        # Load system-delivered classifiers.

        with open('label_candidates.clf', 'rb') as file:
            s = file.read()

        self.__label_classifier = pickle.loads(s)

        with open('error_messages.clf', 'rb') as file:
            s = file.read()

        self.__error_msg_classifier = pickle.loads(s)

        with open('commits.clf', 'rb') as file:
            s = file.read()

        self.__commit_classifier = pickle.loads(s)

        with open('page_titles.clf', 'rb') as file:
            s = file.read()

        self.__page_title_classifier = pickle.loads(s)

        # Load live, trainable classifiers.

        with open('label_candidates_live.clf', 'rb') as file:
            s = file.read()

        self.__label_classifier_live = pickle.loads(s)

        with open('error_messages_live.clf', 'rb') as file:
            s = file.read()

        self.__error_msg_classifier_live = pickle.loads(s)

        with open('commits_live.clf', 'rb') as file:
            s = file.read()

        self.__commit_classifier_live = pickle.loads(s)

        if RUN_LIVE:
            self.__label_classifier = self.__label_classifier_live
            self.__error_msg_classifier = self.__error_msg_classifier_live
            self.__commit_classifier = self.__commit_classifier_live

        pass

    def get_page_titles(self, context, concrete_state):
        data = {
            "pageTitles": []
        }

        df = self.__featurize.convert_to_feature_frame(context, concrete_state, measure_color_distance=False)
        df = self.__frame_mapper.map_page_titles(context, df)

        for data_point in df.values:
            widget_key = data_point[0]
            if data_point[4] == 0.0:
                continue
            data_point = data_point[1:].reshape(1, -1)
            pred = self.__page_title_classifier.predict(data_point)
            if pred[0] == 1:
                data["pageTitles"].append(widget_key)

        return data

    def get_page_analysis(self, context, concrete_state):
        data = {
            "pageTitles": [],
            "labelCandidates": [],
            "errorMessages": [],
            "commits": [],
            "cancels": []
        }

        df = self.__featurize.convert_to_feature_frame(context, concrete_state)
        df_first = self.__frame_mapper.map_label_candidates(context, df)
        df_sec = self.__frame_mapper.map_page_titles(context, df)

        for data_point in df_first.values:
            widget_key = data_point[0]
            if data_point[4] == 0.0:
                continue
            data_point = data_point[1:].reshape(1, -1)
            pred = self.__label_classifier.predict(data_point)
            if pred[0] == 1 and widget_key not in self.negativeStorage["labelCandidates"]:
                print(self.storage)
                data["labelCandidates"].append(widget_key)

        for labelCandidate in self.storage["labelCandidates"]:
            if labelCandidate not in data["labelCandidates"]:
                data["labelCandidates"].append(labelCandidate)

        for data_point in df_first.values:
            widget_key = data_point[0]
            if data_point[4] == 0.0:
                continue
            data_point = data_point[1:].reshape(1, -1)
            pred = self.__error_msg_classifier.predict(data_point)
            if pred[0] == 1 and widget_key not in data["labelCandidates"] and widget_key not in self.negativeStorage["errorMessages"]:
                data["errorMessages"].append(widget_key)
            pred = self.__commit_classifier.predict(data_point)
            if pred[0] == 1 and widget_key not in data["labelCandidates"] and widget_key not in self.negativeStorage["errorMessages"]:
                data["commits"].append(widget_key)

        for errorMessage in self.storage["errorMessages"]:
            if errorMessage not in data["errorMessages"]:
                data["errorMessages"].append(errorMessage)

        for data_point in df_sec.values:
            widget_key = data_point[0]
            if data_point[4] == 0.0:
                continue
            data_point = data_point[1:].reshape(1, -1)
            pred = self.__page_title_classifier.predict(data_point)
            if pred[0] == 1 and widget_key not in self.negativeStorage["pageTitles"]:
                data["pageTitles"].append(widget_key)

        for pageTitle in self.storage["pageTitles"]:
            if pageTitle not in data["pageTitles"]:
                data["pageTitles"].append(pageTitle)

        return data

    def add_element(self, context, element):
        added = False
        print(element)

        target_widget_key = element['id']

        concrete_state = element['state']

        element_class = element['classes'][0]

        df = self.__featurize.convert_to_feature_frame(context, concrete_state)

        df_first = self.__frame_mapper.map_label_candidates(context, df)

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

            s = pickle.dumps(clf)

            with open('error_messages_live.clf', 'wb') as file:
                file.write(s)

        elif element_class == 'labelCandidate':
            self.__label_classifier = clf
            self.__label_classifier_df = df_in_use

            s = pickle.dumps(clf)

            with open('label_candidates_live.clf', 'wb') as file:
                file.write(s)

        elif element_class == 'commit':
            self.__commit_classifier = clf
            self.__commit_classifier_df = df_in_use

            s = pickle.dumps(clf)

            with open('commits_live.clf', 'wb') as file:
                file.write(s)

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

        print("")
        print("Metrics (vs. training set)")
        print("Accuracy (all): " + str(accuracy_score(train_true_y, train_pred_y)))
        print("Accuracy (excluding Nones): " + str(accuracy_score(small_train_true_y, small_train_pred_y)))
        print("")
        print(classification_report(train_true_y, train_pred_y, target_names=target_names))

        train_true_y = [target_names[j] for j in train_true_y]
        train_pred_y = [target_names[j] for j in train_pred_y]
        cm = confusion_matrix(train_true_y, train_pred_y, labels=target_names)
        print_cm(cm, target_names)

        print("Done training")
        print(self.storage)
