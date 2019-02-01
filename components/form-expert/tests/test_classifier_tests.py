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
