#!/usr/bin/env python
import random

__author__ = "DionnyS"
__copyright__ = "Copyright 2018, Ultimate Software Group"
__license__ = "GPL"
__version__ = "0.1.0"

import json
import numpy as np
import tensorflow as tf
from keras.models import load_model


class TestSequenceService:
    def __init__(self, acl):
        self.__acl = acl

        with open('embedding.json') as f:
            data = json.load(f)
            self.char_indices = data['char_indices']
            self.indices_char = data['indices_char']

        self.maxlen = 11
        self.chars = self.char_indices.values()

        self.model = load_model('lstm.h5')
        self.model._make_predict_function()
        self.graph = tf.get_default_graph()

    def predict(self, context, query, num_to_predict):
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
                        x_pred[0, t, self.char_indices[char]] = 1.
                        print("vector[0, {}, {}] = 1".format(t, self.char_indices[char]))

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
