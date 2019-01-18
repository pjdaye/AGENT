import datetime
import json
import os

import bottle
from bottle import post, run, request, response
from pymongo import MongoClient

from classifier import fill_form
from generalizer import generalize_label


MONGO_HOST = os.environ['FORM_EXPERT_HOST'] \
    if 'FORM_EXPERT_HOST' in os.environ else 'mongodb://mongo:27017'
PORT = os.environ['FORM_EXPERT_PORT']  \
    if 'FORM_EXPERT_PORT' in os.environ else 8080
MONGO_DATABASE = os.environ['FORM_EXPERT_DATABASE'] \
    if 'FORM_EXPERT_DATABASE' in os.environ else 'form-expert'

app = bottle.app()


"""
[{
    "label": "city",
    "element": "input-text",
    "value": "hello",
}]
"""
@post('/api/v1/form')
def form_example():
    form = json.load(request.body)
    client = MongoClient(MONGO_HOST)
    db = client.get_database(MONGO_DATABASE)
    form = transform_form(form)
    response.content_type = 'application/json'
    return json.dumps({'form_id': save_form(db, form)})

"""
id: 2084024gj2ogj,
form: [{
    "label": "city",
    "element": "input-text",
    "value": "hello",
}]

{
    _id: 2049g204g90a,
    label: "city",
    values: "Weston", "Miami"
}
"""

"""
[
    {
        "label": "city",
    }
]
"""
@post('/api/v1/fill_form')
def fill_form_endpoint():
    print('BODY: ', request.body)
    form = json.load(request.body)
    client = MongoClient(MONGO_HOST)
    db = client.get_database(MONGO_DATABASE)
    form = transform_form(form)
    forms = db.forms.find({})
    form = fill_form(forms, form)
    print('FINAL', form)
    response.content_type = 'application/json'
    return json.dumps(form)

"""
{
    "city": {
        "label": "city",
        "value": "Weston"
    }
}
"""


def transform_form(form):
    features = []
    form_dict = {}
    for field in form:
        generalized_label = generalize_label(field['label'].lower())
        if generalized_label in features:
            generalized_label += '{}'.format(features.count(generalized_label) + 1)
        features.append(generalized_label)
        form_dict[generalized_label] = field
    list.sort(features)

    return {
        'features': features,
        'form': form_dict,
        'created_at': str(datetime.datetime.utcnow())
    }


def save_form(db, form):
    forms = db.forms
    result = forms.insert_one(form)
    print('SAVED', form)
    return str(result.inserted_id)


def start():
    run(app=app, host='localhost', port=PORT)


if __name__ == '__main__':
    start()
