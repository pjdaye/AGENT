#!/usr/bin/env python
import random

import json
import numpy as np
import tensorflow as tf
from aist_common.log import get_logger
from keras.models import load_model

LOGGER = get_logger('test-generator-service')


class TestGeneratorService:
    def __init__(self):
        with open('json/embedding.json') as f:
            data = json.load(f)
            self.char_indices = data['char_indices']
            self.indices_char = data['indices_char']

        self.maxlen = 11
        self.chars = self.char_indices.values()

        self.model = load_model('json/lstm.h5')

        # noinspection PyProtectedMember
        self.model._make_predict_function()

        self.graph = tf.get_default_graph()

    def predict(self, query, num_to_predict):
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
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)
