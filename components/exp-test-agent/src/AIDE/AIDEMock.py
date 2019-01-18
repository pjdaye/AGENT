import random


class AIDEMock:
    def __init__(self):
        pass

    @staticmethod
    def get_input_types():
        return ['VALID', 'BLANK', 'WHITESPACE', 'INVALID_LONG', 'INVALID_SPECIAL_CHARACTERS', 'INVALID_XSR']

    @staticmethod
    def get_concrete_inputs(label, input_class):
        if input_class == 'VALID':
            return AIDEMock.get_concrete_value(label)
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

    @staticmethod
    def get_concrete_value(label):
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
