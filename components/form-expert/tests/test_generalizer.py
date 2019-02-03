import pytest
from generalizer import generalize_label

test_data = [
    ('enter the email associated with your account', 'email'),
    ('zip code', 'ZIPcode'),
    ('postal code', 'ZIPcode'),
    ('first name', 'firstname'),
    ('last name', 'surname'),
    ('city', 'city'),
    ('reference name', 'name'),
    ('password', 'password'),
    ('username', 'username'),
    ('email', 'e-mail'),
    ('street', 'street'),
    ('street address', 'streetaddress'),
    ('state', 'state'),
    ('country', 'country'),
    ('zip', 'ZIPcode'),
    ('search', 'search'),
    ('apt. number', 'apt'),
    ('credit card number', 'number'),
    ('cvv', 'cvv'),
    ('expiration date', 'date'),
    ('birth date', 'date'),
    ('birthday', 'birthday'),
    ('date of birth', 'date'),
    ('account', 'report'),
    ('dependent', 'dependent'),
    ('job title', 'title'),
    ('title', 'title'),
    ('zip / postal code', 'ZIPcode'),
    ('state / province', 'state')
]


@pytest.mark.parametrize("input_data,expected", test_data)
def test_generalize_label(input_data, expected):
    assert generalize_label(input_data) == expected
