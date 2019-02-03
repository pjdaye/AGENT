import datetime
import json
import os

import bottle
from bottle import get, post, run, request, response
from pymongo import MongoClient

from classifier import fill_form
from generalizer import generalize_label


PORT = os.environ['SERVICE_PORT']  \
    if 'FORM_EXPERT_PORT' in os.environ else 8080
MONGO_HOST = os.environ['FORM_EXPERT_MONGO_URI'] \
    if 'FORM_EXPERT_MONGO_URI' in os.environ else 'mongodb://localhost:27017'
MONGO_DATABASE = os.environ['FORM_EXPERT_DATABASE'] \
    if 'FORM_EXPERT_DATABASE' in os.environ else 'form-expert'

app = bottle.app()


@post('/api/v1/form')
def form_example():
    form = json.load(request.body)
    client = MongoClient(MONGO_HOST)
    db = client.get_database(MONGO_DATABASE)
    form = transform_form(form)
    response.content_type = 'application/json'
    return json.dumps({'form_id': save_form(db, form)})


@post('/api/v1/fill_form')
def fill_form_endpoint():
    form = json.load(request.body)
    client = MongoClient(MONGO_HOST)
    db = client.get_database(MONGO_DATABASE)
    form = transform_form(form)
    forms = db.forms.find({})
    form = fill_form(forms, form)
    response.content_type = 'application/json'
    return json.dumps(form)


@get('/api/v1/health_check')
def health_check():
    return json.dumps({'healthy': True})


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
    return str(result.inserted_id)


def start():
    run(app=app, host='localhost', port=PORT)


if __name__ == '__main__':
    start()
