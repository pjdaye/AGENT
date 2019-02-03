import random
import sys

from Levenshtein import seqratio

from aist_common.log import get_logger

LOGGER = get_logger('classifier')


def levenshtein_distance(a, b):
    """ calculates the Levenshtein distance of two instances

    :param a: The first instance to compare.
    :param b: The second instance to compare.

    :return: The Levenshtein distance of the two instances.
    """

    ratio = seqratio(a, b['features'])
    return 1 - ratio


def get_neighbor(training_set, test_instance):
    """ Returns a nearest neighbor out of a given set. If there are multiple neighbors
    with the same smallest distance, one is chosen randomly.

    :param training_set: The set of instances to choose from.
    :param test_instance: The instance to which a nearest neighbor should be found.

    :return: A randomly chosen nearest neighbor of the given instance.
    """

    nearest_neighbors = []
    min_distance = sys.maxsize
    for instance in training_set:
        dist = levenshtein_distance(test_instance, instance)
        if dist == min_distance:
            nearest_neighbors.append(instance)
        elif dist < min_distance:
            min_distance = dist
            nearest_neighbors = [instance]
    return random.choice(nearest_neighbors)


def fill_form(forms, form):
    forms = list(forms)
    new_form = {}

    def rec_fill_form(form, labels):
        if not labels:
            return new_form
        unfilled_labels = []
        neighbor = get_neighbor(forms, labels)
        if not neighbor:
            LOGGER.info('No neighbors found', labels)
            for label in labels:
                new_form[form['form'][label]['id']] = None
            return new_form
        LOGGER.info('Neighbor', neighbor)
        for label in labels:
            if label in neighbor['form']:
                new_form[form['form'][label]['id']] = neighbor['form'][label]['value']
            else:
                unfilled_labels.append(label)
        LOGGER.info('unfilled', unfilled_labels)
        if len(labels) == len(unfilled_labels):
            for label in unfilled_labels:
                new_form[form['form'][label]['id']] = None
            return new_form
        return rec_fill_form(form, unfilled_labels)

    return rec_fill_form(form, list(form['features']))


def main():
    training = [
        {
            'features': ['cat', 'dog', 'snake'],
            'form': {
                'dog': {
                    'value': 'Large'
                },
                'cat': {
                    'value': 'Small'
                },
                'snake': {
                    'value': 'Creepy'
                }
            }
        },
        {
            'features': ['whale'],
            'form': {
                'whale': {
                    'value': 'Large'
                }
            }
        },
        {
            'features': ['dog', 'snake'],
            'form': {
                'dog': {
                    'value': 'hello'
                },
                'snake': {
                    'value': 'world'
                }
            }
        },
        {
            'features': ['dog', 'snake'],
            'form': {
                'dog': {
                    'value': 'zoe'
                },
                'snake': {
                    'value': 'no'
                }
            }
        },
        {
            'features': ['cat', 'dog'],
            'form': {
                'dog': {
                    'value': 'what'
                },
                'cat': {
                    'value': 'the'
                },
            }
        },
        {
            'features': ['cat', 'dog'],
            'form': {
                'dog': {
                    'value': 'zlos'
                },
                'cat': {
                    'value': 'vows'
                },
            }
        },
        {
            'features': ['dog'],
            'form': {
                'dog': {
                    'value': 'solo'
                }
            }
        },
        {
            'features': ['bill', 'tom', 'jim'],
            'form': {
                'bill': {
                    'value': 'alpha'
                },
                'tom': {
                    'value': 'beta'
                },
                'jim': {
                    'value': 'cain'
                },
            }
        },
        {
            'features': ['bill', 'tom', 'jim'],
            'form': {
                'bill': {
                    'value': 'ze'
                },
                'tom': {
                    'value': 'be'
                },
                'jim': {
                    'value': 'qe'
                },
            }
        },
    ]

    test = {
        'features': ['cat', 'whale', 'dog', 'jim'],
        'form': {
            'dog': {'id': 'test1'},
            'whale': {'id': 'test34'},
            'cat': {'id': 'test2'},
            'jim': {'id': 'test3'}
        }
    }


if __name__ == '__main__':
    main()
