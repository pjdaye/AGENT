from unittest.mock import Mock, patch

import pytest
import service
from pymongo import database


@pytest.fixture
def db_mock(forms_collection_mock):
    db_mock = Mock(spec=database.Database)
    db_mock.forms = forms_collection_mock

    return db_mock


@pytest.fixture
def forms_collection_mock():
    forms_collection_mock = Mock()
    forms_collection_mock.insert_one.return_value.inserted_id = 'id'
    forms_collection_mock.find.return_value = Mock()

    return forms_collection_mock


@patch('service.response')
@patch('service.transform_form')
@patch('service.save_form')
@patch('service.MongoClient')
@patch('service.request')
@patch('service.json')
def test_form_example(
        json_mock,
        request_mock,
        mongo_client_mock,
        save_form_mock,
        transform_form_mock,
        response_mock,
        db_mock
):
    # Arrange
    body_mock = Mock()
    request_mock.body = body_mock
    form_mock = Mock()
    json_mock.load.return_value = form_mock
    json_mock.dumps.return_value = '{"form_id": "id"}'
    mongo_client_mock().get_database.return_value = db_mock
    save_form_mock.return_value = 'id'
    transformed_form_mock = Mock()
    transform_form_mock.return_value = transformed_form_mock

    # Act
    result = service.form_example()

    # Assert
    json_mock.load.assert_called_with(body_mock)
    transform_form_mock.called_with(form_mock)
    save_form_mock.assert_called_with(db_mock, transformed_form_mock)
    json_mock.dumps.assert_called_with({'form_id': 'id'})
    assert response_mock.content_type == 'application/json'
    assert result == '{"form_id": "id"}'


@patch('service.response')
@patch('service.fill_form')
@patch('service.transform_form')
@patch('service.save_form')
@patch('service.MongoClient')
@patch('service.request')
@patch('service.json')
def test_form_example(
        json_mock,
        request_mock,
        mongo_client_mock,
        save_form_mock,
        transform_form_mock,
        fill_form_mock,
        response_mock,
        db_mock,
        forms_collection_mock
):
    # Arrange
    body_mock = Mock()
    request_mock.body = body_mock
    form_mock = Mock()
    json_mock.load.return_value = form_mock
    json_mock.dumps.return_value = '{"id": "value"}'
    mongo_client_mock().get_database.return_value = db_mock
    save_form_mock.return_value = 'id'
    transformed_form_mock = Mock()
    transform_form_mock.return_value = transformed_form_mock
    filled_form_mock = Mock()
    fill_form_mock.return_value = filled_form_mock

    # Act
    result = service.fill_form_endpoint()

    # Assert
    json_mock.load.assert_called_with(body_mock)
    transform_form_mock.called_with(form_mock)
    forms_collection_mock.find.assert_called_with({})
    fill_form_mock.assert_called_with(forms_collection_mock.find.return_value, transformed_form_mock)
    json_mock.dumps.assert_called_with(filled_form_mock)
    assert response_mock.content_type == 'application/json'
    assert result == '{"id": "value"}'


def test_health_check():
    assert service.health_check() == "{\"healthy\": true}"


def test_save_form(db_mock):
    # Arrange
    form_mock = Mock()

    # Act
    result = service.save_form(db_mock, form_mock)

    # Assert
    assert db_mock.forms.insert_one.called is True
    db_mock.forms.insert_one.assert_called_with(form_mock)
    assert result == 'id'
