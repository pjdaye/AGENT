import pandas as pd

from services.concrete_state_featurizer import calc_color_distance, calc_point_distance, sigmoid, get_nearest_color, \
    normalize


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
