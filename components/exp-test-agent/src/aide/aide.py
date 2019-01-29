import random
import requests
import os


class AIDE:
    def __init__(self):
        self.FORM_EXPERT_URL = 'http://form-expert'
        if 'FORM_EXPERT_URL' in os.environ:
            self.FORM_EXPERT_URL = os.environ['FORM_EXPERT_URL']

        self.FILL_FORM_URL = '{}/api/v1/fill_form'.format(self.FORM_EXPERT_URL)

    @staticmethod
    def get_input_types():
        return ['VALID', 'BLANK', 'WHITESPACE', 'INVALID_LONG', 'INVALID_SPECIAL_CHARACTERS', 'INVALID_XSR']

    def get_concrete_inputs(self, label, input_class):
        if input_class == 'VALID':
            return self.get_concrete_value(label)
        elif input_class == 'BLANK':
            values = ['']
            return random.choice(values)
        elif input_class == 'WHITESPACE':
            values = ['  ', '   ',  '       ']
            return random.choice(values)
        elif input_class == 'INVALID_LONG':
            values = ['asdhasdjkashdkjahsdjkhkjashdkajsdhsakjhdjkahsdjkahsdjkhasdjkhasjkdhasjkdhasjkdhasjkdhasjkdhasd']
            return random.choice(values)
        elif input_class == 'INVALID_SPECIAL_CHARACTERS':
            values = ['<!@#!@#9AISD9SID9I9ASDMASD>!!>@>!#!@>#!<@#!<A<A<SD>!!>@#!@<#!@#!@!@J#!JJ@*@#*!#*E!IEID!*#!']
            return random.choice(values)
        elif input_class == 'INVALID_XSR':
            values = ['<script>alert("test");</script>']
            return random.choice(values)

    def get_concrete_value(self, label):

        payload = [
            {
                'label': label,
                'id': label
            }
        ]
        response = requests.post(self.FILL_FORM_URL, json=payload, verify=False)

        if response.status_code == 200 and label in response.json():
            return response.json()[label]

        # Fall back to mock data
        label = label.replace(' ', '').upper()
        if label == "LASTNAME":
            values = ['King', 'Santiago', 'Adamo', 'Briggs', 'Vanderwall', 'Maliani', 'Muras', 'Mattera', 'Alt', 'Phillips', 'Daye', 'Peixoto', 'Pava', 'Dalvi', 'Vaswanathan']
            return random.choice(values)
        elif label == "CITY":
            values = ['Miami', 'New York', 'Chicago', 'Boston', 'Los Angeles']
            return random.choice(values)
        elif label == "FIRSTNAME":
            values = ['Tariq', 'Dionny', 'David', 'Keith', 'Robert', 'John', 'Brian', 'Michael', 'Patrick', 'Justin', 'Phillip', 'Ed', 'Jairo', 'Kaushal', 'Praveen']
            return random.choice(values)
        elif label == "ADDRESS":
            values = ['Address 1', 'Address 2', 'ABC', 'DEF']
            return random.choice(values)
        elif label == "TELEPHONE":
            values = ['123', '4562', '1234', '25123']
            return random.choice(values)
        elif label == "DATE":
            values = ['01/01/2010']
            return random.choice(values)
        elif label == "BIRTHDATE":
            values = ['01/01/2010']
            return random.choice(values)
        elif label == "DESCRIPTION":
            values = ['A simple description']
            return random.choice(values)
        elif label == "NAME":
            values = ['Lucky', 'Lucy', 'Lexi']
            return random.choice(values)
        return None
