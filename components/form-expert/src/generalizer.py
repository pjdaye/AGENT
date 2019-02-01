import re

from nltk.corpus import wordnet
import spacy

print('Loading Spacy EN')
en_nlp = spacy.load('en')


def generalize_label(input_label):
    result = input_label
    friendly_label = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', input_label)[0].rstrip()
    nums = [int(s) for s in input_label.split() if s.isdigit()]
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


def main():
    test_set = [
        'enter the email associated with your account',
        'zip code',
        'postal code',
        'first name',
        'last name',
        'city',
        'reference name',
        'password',
        'username',
        'email',
        'street',
        'street address',
        'state',
        'country',
        'zip',
        'search',
        'apt. number',
        'credit card number',
        'cvv',
        'expiration date',
        'birth date',
        'birthday',
        'date of birth',
        'account',
        'dependent',
        'job title',
        'title',
         'zip / postal code',
         'state / province']
    for test in test_set:
        print(generalize_label(test))


if __name__ == '__main__':
    main()
