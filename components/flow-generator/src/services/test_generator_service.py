"""Handles abstract test flow generation requests."""
import os
import random

import json
import numpy as np
import tensorflow as tf
from aist_common.log import get_logger
from keras.models import load_model

LOGGER = get_logger('test-generator-service')

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))


class TestGeneratorService:
    """Handles abstract test flow generation requests."""

    def __init__(self):
        """ Initializes the TestGeneratorService class.
        """

        with open(f'{BASE_PATH}/embedding.json') as f:
            data = json.load(f)
            self.char_indices = data['char_indices']
            self.indices_char = data['indices_char']

        self.maxlen = 11
        self.chars = self.char_indices.values()

        self.model = load_model(f'{BASE_PATH}/lstm.h5')

        # noinspection PyProtectedMember
        self.model._make_predict_function()

        self.graph = tf.get_default_graph()

    def predict(self, query, num_to_predict):
        """ Relies on an underlying pre-trained long short-term memory-based (LSTM) recurrent
            neural network (RNN) to generate an abstract test flow of maximum length self.maxlen.
            Invokes the LSTM up to maxlen times.

            Example:
            Given a query such as “Observe TextBox” consisting of 2 words, we invoke the LSTM 9 times,
            each time appending the predicted word to the query for the next prediction step.

        :param query: The beginning of the sentence to start generating from.

        :param num_to_predict: The number of abstract test flow sentences to generate.

        :return: A generated abstract test flow sentence.
        """

        output = []

        for i in range(num_to_predict):
            rand = random.randint(1, 9999)
            print(rand)
            tf.set_random_seed(rand)

            generated = []

            generated.extend(query)

            with self.graph.as_default():
                for i in range(self.maxlen - len(query)):
                    x_pred = np.zeros((1, self.maxlen, len(self.chars)))
                    for t, char in enumerate(query):

                        if char not in self.char_indices:
                            LOGGER.warning("Unsupported query token: {}. LSTM retraining will be necessary."
                                           .format(char.upper()))

                            return output

                        x_pred[0, t, self.char_indices[char]] = 1.

                    preds = self.model.predict(x_pred, verbose=0)[0]

                    next_index = self.sample(preds, 0.2)
                    next_char = self.indices_char[str(next_index)]

                    generated.extend([next_char])
                    query.extend([next_char])

            output.append(generated)

        return output

    def sample(self, preds, temperature=1.0):
        """ Controls LSTM prediction randomness by scaling the logits prior to applying softmax.

        :param preds: A set of generated predictions.
        :param temperature: Hyper-parameter used to control prediction randomness.

        :return: A final prediction from the set of possible predictions.
        """

        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)
