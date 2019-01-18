import math

__author__ = "RobertV"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"


def cosine_similarity(first_vector, second_vector):
    first_vector, second_vector = _pad_vectors(first_vector, second_vector)
    dot_product_val = float(dot_product(first_vector, second_vector))

    first_vector_magnitude = magnitude(first_vector)
    second_vector_magnitude = magnitude(second_vector)

    cosine_sim = dot_product_val / (first_vector_magnitude * second_vector_magnitude)

    return cosine_sim


def dot_product(first_vector, second_vector):
    assert len(first_vector) == len(second_vector)

    dot_product_val = 0
    for dimension in first_vector:
        dot_product_val = dot_product_val + (first_vector[dimension] * second_vector[dimension])

    return dot_product_val


def _pad_vectors(first_vector, second_vector):
    padded_first_vector = {}
    padded_second_vector = {}
    for dimension in first_vector:
        padded_first_vector[dimension] = first_vector[dimension]
        if dimension not in second_vector:
            padded_second_vector[dimension] = 0

    for dimension in second_vector:
        padded_second_vector[dimension] = second_vector[dimension]
        if dimension not in first_vector:
            padded_first_vector[dimension] = 0

    return padded_first_vector, padded_second_vector


def magnitude(vector):
    sum_of_squares = 0
    for dimension in vector:
        sum_of_squares = sum_of_squares + (vector[dimension] * vector[dimension])

    return math.sqrt(sum_of_squares)
