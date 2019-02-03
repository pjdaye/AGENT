import math
from unittest import mock
import classifier


def levenshtein_distance_side_effect(a, b):
    if a == 2 and b == 2:
        return 0.3
    return 0


def test_levenshtein_distance():
    # Arrange
    a = 2
    b = {
        'features': 2
    }

    # Act
    with mock.patch('classifier.seqratio', side_effect=levenshtein_distance_side_effect):
        result = classifier.levenshtein_distance(a, b)

    # Assert
    assert result == 0.7


instance_1 = 1
instance_2 = 2
instance_3 = 3
instance_4 = 4
instance_5 = 6

instances = [
    instance_1,
    instance_2,
    instance_3,
    instance_4
]


def get_neighbor_side_effect(a, b):
    return math.fabs(a - b)


def test_get_neighbor_first_instance():
    # Arrange
    test_instance = 0

    # Act
    with mock.patch('classifier.levenshtein_distance', side_effect=get_neighbor_side_effect):
        nearest_neighbor = classifier.get_neighbor(instances, test_instance)

    # Assert
    assert nearest_neighbor == 1


def test_get_neighbor_instance_in_the_middle():
    # Arrange
    test_instance = 3

    # Act
    with mock.patch('classifier.levenshtein_distance', side_effect=get_neighbor_side_effect):
        nearest_neighbor = classifier.get_neighbor(instances, test_instance)

    # Assert
    assert nearest_neighbor == 3


def test_get_neighbor_multiple_nearest_neighbors():
    # Arrange
    test_instance = 5

    # Act
    with mock.patch('classifier.levenshtein_distance', side_effect=get_neighbor_side_effect):
        nearest_neighbor = classifier.get_neighbor(instances, test_instance)

    # Assert
    assert nearest_neighbor == 4 or nearest_neighbor == 6
