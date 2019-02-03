import re

from nltk.corpus import wordnet
import spacy

print('Loading Spacy EN')
en_nlp = spacy.load('en')


def generalize_label(input_label):
    """Generalizes labels so that similar form inputs can be mapped.

    :param input_label: The label to generalize.
    :return: The generalized form of the label.
    """

    result = input_label
    friendly_label = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', input_label)[0].rstrip()
    syns = wordnet.synsets(friendly_label.replace(' ', '_'))
    doc = en_nlp(input_label)

    sentence = next(doc.sents)
    nsubj = None
    dobj = None
    root = None
    for word in sentence:
        if word.dep_ == 'nsubj':
            nsubj = word.lemma_
        if word.dep_ == 'dobj':
            dobj = word.lemma_
        elif word.dep_ == 'ROOT':
            root = word.lemma_

    if len(syns) == 1:
        result = syns[0].lemmas()[0].name()
    elif len(syns) > 1:
        result = syns[1].lemmas()[0].name()
    elif nsubj is not None:
        result = nsubj
    elif dobj is not None:
        result = dobj
    elif root is not None:
        result = root
    return result.replace('_', '')
