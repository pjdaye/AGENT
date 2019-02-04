import math
from unittest import mock
from unittest.mock import patch, call

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


@patch('classifier.get_neighbor')
def test_fill_form_empty_form(_):
    # Arrange
    forms = []
    form = {
        'features': []
    }

    # Act
    result = classifier.fill_form(forms, form)

    # Assert
    assert len(result) == 0


@patch('classifier.get_neighbor')
def test_fill_form_no_neighbor_found(get_neighbor_mock):
    # Arrange
    forms = []
    form = {
        'features': [
            'g_label_a',
            'g_label_b'
        ],
        'form': {
            'g_label_a': {
                'id': 'id_a'
            },
            'g_label_b': {
                'id': 'id_b'
            }
        }
    }
    get_neighbor_mock.return_value = None

    # Act
    result = classifier.fill_form(forms, form)

    # Assert
    assert len(result) == 2
    assert result['id_a'] is None
    assert result['id_b'] is None


@patch('classifier.LOGGER')
@patch('classifier.get_neighbor')
def test_fill_form_nearest_neighbor_does_not_provide_matching_fields(get_neighbor_mock, logger_mock):
    # Arrange
    forms = []
    form = {
        'features': [
            'g_label_a',
            'g_label_b'
        ],
        'form': {
            'g_label_a': {
                'id': 'id_a'
            },
            'g_label_b': {
                'id': 'id_b'
            }
        }
    }
    get_neighbor_mock.return_value = {
        'form': {
            'g2_label_a': 'value1',
            'g2_label_b': 'value2'
        }
    }

    # Act
    result = classifier.fill_form(forms, form)

    # Assert
    assert len(result) == 2
    assert result['id_a'] is None
    assert result['id_b'] is None
    logger_mock.info\
        .assert_called_with('unfilled', ['g_label_a', 'g_label_b'])


@patch('classifier.LOGGER')
@patch('classifier.get_neighbor')
def test_fill_form_recursive_call_completes_form(get_neighbor_mock, logger_mock):
    # Arrange
    forms = []
    form = {
        'features': [
            'g_label_a',
            'g_label_b'
        ],
        'form': {
            'g_label_a': {
                'id': 'id_a'
            },
            'g_label_b': {
                'id': 'id_b'
            }
        }
    }
    get_neighbor_mock.side_effect = [
        {
            'form': {
                'g_label_a': {
                    'value': 'value1'
                }
            }
        },
        {
            'form': {
                'g_label_b': {
                    'value': 'value2'
                }
            }
        }
    ]

    # Act
    result = classifier.fill_form(forms, form)

    # Assert
    assert len(result) == 2
    assert result['id_a'] == 'value1'
    assert result['id_b'] == 'value2'
    logger_mock.info.assert_has_calls(
        [
            call('Neighbor', {
                'form': {
                    'g_label_a': {
                        'value': 'value1'
                    }
                }
            }),
            call('unfilled', ['g_label_b']),
            call('Neighbor', {
                'form': {
                    'g_label_b': {
                        'value': 'value2'
                    }
                }
            }),
            call('unfilled', [])
        ]
    )
