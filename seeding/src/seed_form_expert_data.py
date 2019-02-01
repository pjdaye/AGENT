import os
import json
import requests


class FormExpertSeeder:

    def __init__(self):
        self.FORM_EXPERT_URL = 'http://form-expert'
        if 'FORM_EXPERT_URL' in os.environ:
            self.FORM_EXPERT_URL = os.environ['FORM_EXPERT_URL']

        self.POST_FORM_URL = '{}/api/v1/form'.format(self.FORM_EXPERT_URL)

    def seed(self):
        with open('forms.json', 'r') as f:
            forms = json.load(f)

        for form in forms:
            response = requests.post(self.POST_FORM_URL, json=form, verify=False)
            if response.status_code is 200:
                print("Seeded form successfully")
            else:
                print("Error seeding form")


def generate_form():
    data = {
        '_id': ''
    }
    return data


FormExpertSeeder().seed()
