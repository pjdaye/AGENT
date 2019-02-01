import json

import pandas as pd
import pytest

from services.concrete_state_featurizer import calc_color_distance, calc_point_distance, sigmoid, get_nearest_color, \
    normalize, ConcreteStateFeaturize, basic_html_tags


class TestConcreteStateFeaturize:
    def test_calc_color_distance_same_color(self):
        # Arrange
        color_1 = [100, 100, 100]
        color_2 = [100, 100, 100]

        # Act
        dist = calc_color_distance(color_1, color_2)

        # Assert
        assert dist == 0.0

    def test_calc_color_distance_similar_colors(self):
        # Arrange
        color_1 = [101, 100, 100]
        color_2 = [100, 100, 100]

        # Act
        dist = calc_color_distance(color_1, color_2)

        # Assert
        assert 0.0 < dist < 30.0

    def test_calc_color_distance_different_colors(self):
        # Arrange
        color_1 = [0, 100, 100]
        color_2 = [100, 100, 100]

        # Act
        dist = calc_color_distance(color_1, color_2)

        # Assert
        assert 30.0 < dist < 50.0

    def test_calc_point_distance_zero_distance(self):
        # Act.
        dist = calc_point_distance(50, 50, 50, 50)

        # Assert.
        assert dist == 0.0

    def test_calc_point_distance_non_zero_distance(self):
        # Act.
        dist = calc_point_distance(50, 50, 55, 55)

        # Assert.
        assert dist == 7.0710678118654755

    def test_sigmoid_zero(self):
        # Act.
        sig = sigmoid(0)

        # Assert.
        assert sig == 0.5

    def test_sigmoid_one(self):
        # Act.
        sig = sigmoid(1)

        # Assert.
        assert sig == 0.7310585786300049

    def test_get_nearest_color_red(self):
        # Arrange.
        color = "rgb(255, 0, 0)"

        # Act.
        nearest = get_nearest_color(color)

        # Assert.
        assert nearest == "red"

    def test_get_nearest_color_rgba(self):
        # Arrange.
        color = "rgb(255, 0, 0, 1)"

        # Act.
        nearest = get_nearest_color(color)

        # Assert.
        assert nearest == "red"

    def test_get_nearest_color_shade_of_red(self):
        # Arrange.
        color = "rgb(196, 31, 31)"

        # Act.
        nearest = get_nearest_color(color)

        # Assert.
        assert nearest == "red"

    def test_get_nearest_color_shade_of_grey(self):
        # Arrange.
        color = "rgb(147, 144, 144)"

        # Act.
        nearest = get_nearest_color(color)

        # Assert.
        assert nearest == "grey"

    def test_get_nearest_color_invalid_format(self):
        # Arrange.
        color = "rgb"

        # Act.
        nearest = get_nearest_color(color)

        # Assert.
        assert nearest == "black"

    def test_normalize(self):
        # Arrange.
        my_dict = {
            'name': ["a", "b", "c", "d", "e", "f", "g"],
            'age': [20, 27, 35, 55, 18, 21, 35],
            'designation': ["VP", "CEO", "CFO", "VP", "VP", "CEO", "MD"]
        }

        df = pd.DataFrame(my_dict)

        # Act.
        df = normalize(df, ['name', 'designation'])

        # Assert.
        assert df['age'][0] == 0.0541
        assert df['age'][1] == 0.2432
        assert df['age'][2] == 0.4595
        assert df['age'][3] == 1.0000
        assert df['age'][4] == 0.0000
        assert df['age'][5] == 0.0811
        assert df['age'][6] == 0.4595

    def test_normalize_with_non_excluded_non_numeric_data(self):
        # Arrange.
        my_dict = {
            'name': ["a", "b", "c", "d", "e", "f", "g"],
            'age': [20, 27, 35, 55, 18, 21, 35],
            'designation': ["VP", "CEO", "CFO", "VP", "VP", "CEO", "MD"]
        }

        df = pd.DataFrame(my_dict)

        # Act.
        with pytest.raises(Exception) as e_info:
            normalize(df, ['name'])

        # Assert.
        assert str(e_info.value) == 'Error normalizing feature: designation'

    def test_convert_to_feature_frame_single_widget(self):
        # Arrange.
        with open('data/single_widget.json') as file:
            json_data = json.loads(file.read())

        # Act.
        df = ConcreteStateFeaturize.convert_to_feature_frame(json_data)

        # Assert.
        assert df.shape[0] == 3
        assert df.shape[1] == 16
        assert 'Key' in df.columns.values
        assert 'Tag' in df.columns.values
        assert 'Parent_Tag' in df.columns.values
        assert 'Attr_For' in df.columns.values
        assert 'Num_Children' in df.columns.values
        assert 'Num_Siblings' in df.columns.values
        assert 'Depth' in df.columns.values
        assert 'X_Percent' in df.columns.values
        assert 'Y_Percent' in df.columns.values
        assert 'Font_Size' in df.columns.values
        assert 'Font_Weight' in df.columns.values
        assert 'Is_Text' in df.columns.values
        assert 'Nearest_Color' in df.columns.values
        assert 'Nearest_Bg_Color' in df.columns.values
        assert 'Distance_From_Input' in df.columns.values
        assert 'Text' in df.columns.values

        assert df['Key'][0] == "DIV0_0_1_0_0_0:4"
        assert df['Key'][1] == "LABEL0_0_1_0_0_0_0_0_0_1_1_0:10"
        assert df['Key'][2] == "INPUTusername0_0_1_0_0_0_0_0_0_1_1_1:10"

        assert df['Tag'][0] == basic_html_tags.index('div') + 1
        assert df['Tag'][1] == basic_html_tags.index('label') + 1
        assert df['Tag'][2] == basic_html_tags.index('input') + 1

        assert df['Parent_Tag'][0] == 0
        assert df['Parent_Tag'][1] == basic_html_tags.index('div') + 1
        assert df['Parent_Tag'][2] == basic_html_tags.index('div') + 1

        assert df['Attr_For'][0] == 0.0
        assert df['Attr_For'][1] == 1.0
        assert df['Attr_For'][2] == 0.0

        # Num Children is normalized.
        assert df['Num_Children'][0] == 1.0
        assert df['Num_Children'][1] == 0.5
        assert df['Num_Children'][2] == 0.0

        # Num Siblings is normalized.
        assert df['Num_Siblings'][0] == 0.0
        assert df['Num_Siblings'][1] == 1.0
        assert df['Num_Siblings'][2] == 1.0

        # Depth is normalized.
        assert df['Depth'][0] == 0.0
        assert df['Depth'][1] == 1.0
        assert df['Depth'][2] == 1.0

        # X_Percent is normalized.
        assert df['X_Percent'][0] == 0.0
        assert df['X_Percent'][1] == 1.0
        assert df['X_Percent'][2] == 1.0

        # Y_Percent is normalized.
        assert df['Y_Percent'][0] == 0.0
        assert df['Y_Percent'][1] == 0.875
        assert df['Y_Percent'][2] == 1.0

        # Font Size is normalized.
        assert df['Font_Size'][0] == 0.0
        assert df['Font_Size'][1] == 1.0
        assert df['Font_Size'][2] == 0.5556

        # Font Weight is normalized.
        assert df['Font_Weight'][0] == 0.3333
        assert df['Font_Weight'][1] == 1.0
        assert df['Font_Weight'][2] == 0.0

        assert df['Is_Text'][0] == 0.0
        assert df['Is_Text'][1] == 1.0
        assert df['Is_Text'][2] == 0.0

        assert df['Nearest_Color'][0] == "grey"
        assert df['Nearest_Color'][1] == "grey"
        assert df['Nearest_Color'][2] == "grey"

        assert df['Nearest_Bg_Color'][0] == "black"
        assert df['Nearest_Bg_Color'][1] == "black"
        assert df['Nearest_Bg_Color'][2] == "white"

        # Distance From Input is normalized.
        assert df['Distance_From_Input'][0] == 1.0
        assert df['Distance_From_Input'][1] == 0.0325
        assert df['Distance_From_Input'][2] == 0.0

        assert df['Text'][0] == ""
        assert df['Text'][1] == "Username"
        assert df['Text'][2] == ""

    def test_convert_to_feature_frame_without_color_measurements(self):
        # Arrange.
        with open('data/single_widget.json') as file:
            json_data = json.loads(file.read())

        # Act.
        df = ConcreteStateFeaturize.convert_to_feature_frame(json_data, measure_color_distance=False)

        # Assert.
        assert df.shape[0] == 3
        assert df.shape[1] == 16
        assert 'Key' in df.columns.values
        assert 'Tag' in df.columns.values
        assert 'Parent_Tag' in df.columns.values
        assert 'Attr_For' in df.columns.values
        assert 'Num_Children' in df.columns.values
        assert 'Num_Siblings' in df.columns.values
        assert 'Depth' in df.columns.values
        assert 'X_Percent' in df.columns.values
        assert 'Y_Percent' in df.columns.values
        assert 'Font_Size' in df.columns.values
        assert 'Font_Weight' in df.columns.values
        assert 'Is_Text' in df.columns.values
        assert 'Nearest_Color' in df.columns.values
        assert 'Nearest_Bg_Color' in df.columns.values
        assert 'Distance_From_Input' in df.columns.values
        assert 'Text' in df.columns.values

        assert df['Key'][0] == "DIV0_0_1_0_0_0:4"
        assert df['Key'][1] == "LABEL0_0_1_0_0_0_0_0_0_1_1_0:10"
        assert df['Key'][2] == "INPUTusername0_0_1_0_0_0_0_0_0_1_1_1:10"

        assert df['Tag'][0] == basic_html_tags.index('div') + 1
        assert df['Tag'][1] == basic_html_tags.index('label') + 1
        assert df['Tag'][2] == basic_html_tags.index('input') + 1

        assert df['Parent_Tag'][0] == 0
        assert df['Parent_Tag'][1] == basic_html_tags.index('div') + 1
        assert df['Parent_Tag'][2] == basic_html_tags.index('div') + 1

        assert df['Attr_For'][0] == 0.0
        assert df['Attr_For'][1] == 1.0
        assert df['Attr_For'][2] == 0.0

        # Num Children is normalized.
        assert df['Num_Children'][0] == 1.0
        assert df['Num_Children'][1] == 0.5
        assert df['Num_Children'][2] == 0.0

        # Num Siblings is normalized.
        assert df['Num_Siblings'][0] == 0.0
        assert df['Num_Siblings'][1] == 1.0
        assert df['Num_Siblings'][2] == 1.0

        # Depth is normalized.
        assert df['Depth'][0] == 0.0
        assert df['Depth'][1] == 1.0
        assert df['Depth'][2] == 1.0

        # X_Percent is normalized.
        assert df['X_Percent'][0] == 0.0
        assert df['X_Percent'][1] == 1.0
        assert df['X_Percent'][2] == 1.0

        # Y_Percent is normalized.
        assert df['Y_Percent'][0] == 0.0
        assert df['Y_Percent'][1] == 0.875
        assert df['Y_Percent'][2] == 1.0

        # Font Size is normalized.
        assert df['Font_Size'][0] == 0.0
        assert df['Font_Size'][1] == 1.0
        assert df['Font_Size'][2] == 0.5556

        # Font Weight is normalized.
        assert df['Font_Weight'][0] == 0.3333
        assert df['Font_Weight'][1] == 1.0
        assert df['Font_Weight'][2] == 0.0

        assert df['Is_Text'][0] == 0.0
        assert df['Is_Text'][1] == 1.0
        assert df['Is_Text'][2] == 0.0

        assert df['Nearest_Color'][0] == "black"
        assert df['Nearest_Color'][1] == "black"
        assert df['Nearest_Color'][2] == "black"

        assert df['Nearest_Bg_Color'][0] == "black"
        assert df['Nearest_Bg_Color'][1] == "black"
        assert df['Nearest_Bg_Color'][2] == "black"

        # Distance From Input is normalized.
        assert df['Distance_From_Input'][0] == 1.0
        assert df['Distance_From_Input'][1] == 0.0325
        assert df['Distance_From_Input'][2] == 0.0

        assert df['Text'][0] == ""
        assert df['Text'][1] == "Username"
        assert df['Text'][2] == ""

    def test_convert_to_feature_frame_with_empty_for_attribute(self):
        # Arrange.
        with open('data/empty_for_attribute.json') as file:
            json_data = json.loads(file.read())

        # Act.
        df = ConcreteStateFeaturize.convert_to_feature_frame(json_data, measure_color_distance=False)

        # Assert.
        assert df.shape[0] == 3
        assert df.shape[1] == 16
        assert 'Key' in df.columns.values
        assert 'Attr_For' in df.columns.values

        assert df['Key'][0] == "DIV0_0_1_0_0_0:4"
        assert df['Key'][1] == "LABEL0_0_1_0_0_0_0_0_0_1_1_0:10"
        assert df['Key'][2] == "INPUTusername0_0_1_0_0_0_0_0_0_1_1_1:10"

        assert df['Attr_For'][0] == 0.0
        assert df['Attr_For'][1] == 0.0
        assert df['Attr_For'][2] == 0.0

    def test_convert_to_feature_frame_with_equal_min_max_during_normalize(self):
        # Arrange.
        with open('data/min_equal_max_normalize.json') as file:
            json_data = json.loads(file.read())

        # Act.
        df = ConcreteStateFeaturize.convert_to_feature_frame(json_data, measure_color_distance=False)

        # Assert.
        assert df.shape[0] == 3
        assert df.shape[1] == 16
        assert 'Key' in df.columns.values
        assert 'Tag' in df.columns.values
        assert 'Parent_Tag' in df.columns.values
        assert 'Attr_For' in df.columns.values
        assert 'Num_Children' in df.columns.values
        assert 'Num_Siblings' in df.columns.values
        assert 'Depth' in df.columns.values
        assert 'X_Percent' in df.columns.values
        assert 'Y_Percent' in df.columns.values
        assert 'Font_Size' in df.columns.values
        assert 'Font_Weight' in df.columns.values
        assert 'Is_Text' in df.columns.values
        assert 'Nearest_Color' in df.columns.values
        assert 'Nearest_Bg_Color' in df.columns.values
        assert 'Distance_From_Input' in df.columns.values
        assert 'Text' in df.columns.values

        assert df['Key'][0] == "DIV0_0_1_0_0_0:4"
        assert df['Key'][1] == "LABEL0_0_1_0_0_0_0_0_0_1_1_0:10"
        assert df['Key'][2] == "INPUTusername0_0_1_0_0_0_0_0_0_1_1_1:10"

        # Font Size is normalized.
        assert df['Font_Size'][0] == 1.0
        assert df['Font_Size'][1] == 1.0
        assert df['Font_Size'][2] == 1.0

    def test_convert_to_feature_frame(self):
        # Arrange.
        with open('data/login_page.json') as file:
            json_data = json.loads(file.read())

        # Act.
        df = ConcreteStateFeaturize.convert_to_feature_frame(json_data)

        # Assert.
        assert df.shape[0] == 14
        assert df.shape[1] == 16
        assert 'Key' in df.columns.values
        assert 'Tag' in df.columns.values
        assert 'Parent_Tag' in df.columns.values
        assert 'Attr_For' in df.columns.values
        assert 'Num_Children' in df.columns.values
        assert 'Num_Siblings' in df.columns.values
        assert 'Depth' in df.columns.values
        assert 'X_Percent' in df.columns.values
        assert 'Y_Percent' in df.columns.values
        assert 'Font_Size' in df.columns.values
        assert 'Font_Weight' in df.columns.values
        assert 'Is_Text' in df.columns.values
        assert 'Nearest_Color' in df.columns.values
        assert 'Nearest_Bg_Color' in df.columns.values
        assert 'Distance_From_Input' in df.columns.values
        assert 'Text' in df.columns.values
        print(df.to_string())
