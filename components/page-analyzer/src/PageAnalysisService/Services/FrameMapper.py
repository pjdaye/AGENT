

class FrameMapper:
    @staticmethod
    def map_label_candidates(data_frame):
        feature_mapping = {
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
                "LabelCandidate": 1
            },
        }

        df = data_frame.copy()
        df.replace(feature_mapping, inplace=True)

        for col in ['Tag', 'Parent_Tag', 'Num_Children', 'Num_Siblings', 'Depth', 'X_Percent', 'Y_Percent', 'Text']:
            del df[col]

        return df

    @staticmethod
    def map_page_titles(data_frame):
        feature_mapping = {
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
                "PageTitle": 1
            },
        }

        df = data_frame.copy()
        df.replace(feature_mapping, inplace=True)

        for col in df:
            match = False
            for inner_col in ['Key', 'Tag', 'Is_Text', 'Font_Weight', 'Font_Size', 'Distance_From_Input']:
                if col == inner_col:
                    match = True
            if not match:
                del df[col]

        return df
