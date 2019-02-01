import json
import os
import shutil

from distutils.dir_util import copy_tree

from services.page_analysis_service import PageAnalysisService


class TestPageAnalyzer:
    BASE_PATH = None
    BACKUP_PATH = None

    @classmethod
    def setup_class(cls):
        cls.BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
        cls.BACKUP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'backup'))
        copy_tree(cls.BASE_PATH, cls.BACKUP_PATH)

    @classmethod
    def teardown_class(cls):
        copy_tree(cls.BACKUP_PATH, cls.BASE_PATH)
        shutil.rmtree(cls.BACKUP_PATH)

    def test_get_page_titles(self):
        # Arrange.
        with open('json/login_page.json') as file:
            json_data = json.loads(file.read())

        # Act.
        page_titles = PageAnalysisService(base_path=TestPageAnalyzer.BASE_PATH).get_page_titles(json_data)

        # Assert.
        assert 'H20_0_1_0_0_0_0_0_0_0:8' in page_titles['pageTitles']
        assert json_data['widgets']['H20_0_1_0_0_0_0_0_0_0:8']['properties']['text'] == 'Task Manager'

    def test_get_page_analysis(self):
        # Arrange.
        with open('json/pet_clinic_form.json') as file:
            json_data = json.loads(file.read())

        # Act.
        classes = PageAnalysisService().get_page_analysis(json_data)

        # Assert.
        assert len(classes['pageTitles']) == 1
        assert len(classes['labelCandidates']) == 5
        assert len(classes['commits']) == 1
        assert len(classes['errorMessages']) == 0
        assert len(classes['cancels']) == 0

        assert 'H20_0_1_1_0_0:4' in classes['pageTitles']
        assert json_data['widgets']['H20_0_1_1_0_0:4']['properties']['text'] == 'Owner'

        assert 'LABEL0_0_1_1_0_1_0_0_0:7' in classes['labelCandidates']
        assert json_data['widgets']['LABEL0_0_1_1_0_1_0_0_0:7']['properties']['text'] == 'First Name'

        assert 'LABEL0_0_1_1_0_1_0_1_0:7' in classes['labelCandidates']
        assert json_data['widgets']['LABEL0_0_1_1_0_1_0_1_0:7']['properties']['text'] == 'Last Name'

        assert 'LABEL0_0_1_1_0_1_0_2_0:7' in classes['labelCandidates']
        assert json_data['widgets']['LABEL0_0_1_1_0_1_0_2_0:7']['properties']['text'] == 'Address'

        assert 'LABEL0_0_1_1_0_1_0_3_0:7' in classes['labelCandidates']
        assert json_data['widgets']['LABEL0_0_1_1_0_1_0_3_0:7']['properties']['text'] == 'City'

        assert 'LABEL0_0_1_1_0_1_0_4_0:7' in classes['labelCandidates']
        assert json_data['widgets']['LABEL0_0_1_1_0_1_0_4_0:7']['properties']['text'] == 'Telephone'

        assert 'BUTTON0_0_1_1_0_1_1_0_0:7' in classes['commits']
        assert json_data['widgets']['BUTTON0_0_1_1_0_1_1_0_0:7']['properties']['text'] == 'Add Owner'

    def test_add_element_invokes_training(self):
        # Arrange.
        with open('json/pet_clinic_form.json') as file:
            pet_clinic_form = json.loads(file.read())

        with open('json/train_payload_1.json') as file:
            train_payload_1 = json.loads(file.read())

        with open('json/train_payload_2.json') as file:
            train_payload_2 = json.loads(file.read())

        service = PageAnalysisService(base_path=TestPageAnalyzer.BASE_PATH)

        # Act.
        classes_before = service.get_page_analysis(pet_clinic_form)
        service.add_element(train_payload_1)
        service.add_element(train_payload_2)
        classes = service.get_page_analysis(pet_clinic_form)

        # Assert.
        assert len(classes_before['pageTitles']) == 1
        assert len(classes_before['labelCandidates']) == 0
        assert len(classes_before['commits']) == 1
        assert len(classes_before['errorMessages']) == 0
        assert len(classes_before['cancels']) == 0

        assert 'H20_0_1_1_0_0:4' in classes_before['pageTitles']
        assert pet_clinic_form['widgets']['H20_0_1_1_0_0:4']['properties']['text'] == 'Owner'

        assert len(classes_before['labelCandidates']) == 0

        assert 'BUTTON0_0_1_1_0_1_1_0_0:7' in classes_before['commits']
        assert pet_clinic_form['widgets']['BUTTON0_0_1_1_0_1_1_0_0:7']['properties']['text'] == 'Add Owner'

        # After training.
        assert len(classes['pageTitles']) == 1
        assert len(classes['labelCandidates']) == 5
        assert len(classes['commits']) == 1
        assert len(classes['errorMessages']) == 0
        assert len(classes['cancels']) == 0

        assert 'H20_0_1_1_0_0:4' in classes['pageTitles']
        assert pet_clinic_form['widgets']['H20_0_1_1_0_0:4']['properties']['text'] == 'Owner'

        assert 'LABEL0_0_1_1_0_1_0_0_0:7' in classes['labelCandidates']
        assert pet_clinic_form['widgets']['LABEL0_0_1_1_0_1_0_0_0:7']['properties']['text'] == 'First Name'

        assert 'LABEL0_0_1_1_0_1_0_1_0:7' in classes['labelCandidates']
        assert pet_clinic_form['widgets']['LABEL0_0_1_1_0_1_0_1_0:7']['properties']['text'] == 'Last Name'

        assert 'LABEL0_0_1_1_0_1_0_2_0:7' in classes['labelCandidates']
        assert pet_clinic_form['widgets']['LABEL0_0_1_1_0_1_0_2_0:7']['properties']['text'] == 'Address'

        assert 'LABEL0_0_1_1_0_1_0_3_0:7' in classes['labelCandidates']
        assert pet_clinic_form['widgets']['LABEL0_0_1_1_0_1_0_3_0:7']['properties']['text'] == 'City'

        assert 'LABEL0_0_1_1_0_1_0_4_0:7' in classes['labelCandidates']
        assert pet_clinic_form['widgets']['LABEL0_0_1_1_0_1_0_4_0:7']['properties']['text'] == 'Telephone'

        assert 'BUTTON0_0_1_1_0_1_1_0_0:7' in classes['commits']
        assert pet_clinic_form['widgets']['BUTTON0_0_1_1_0_1_1_0_0:7']['properties']['text'] == 'Add Owner'

    def test_add_element_different_classes(self):
        # Arrange.
        with open('json/pet_clinic_complex.json') as file:
            pet_clinic_form = json.loads(file.read())

        with open('json/multi_class_train_1.json') as file:
            train_payload_1 = json.loads(file.read())

        with open('json/multi_class_train_2.json') as file:
            train_payload_2 = json.loads(file.read())

        with open('json/multi_class_train_3.json') as file:
            train_payload_3 = json.loads(file.read())

        with open('json/multi_class_train_4.json') as file:
            train_payload_4 = json.loads(file.read())

        with open('json/multi_class_train_5.json') as file:
            train_payload_5 = json.loads(file.read())

        service = PageAnalysisService(base_path=TestPageAnalyzer.BASE_PATH)

        # Act.
        classes_before = service.get_page_analysis(pet_clinic_form)

        # Label candidate.
        service.add_element(train_payload_1)

        # Label candidate.
        service.add_element(train_payload_2)

        # Error message.
        service.add_element(train_payload_3)

        # Error message.
        service.add_element(train_payload_4)

        # Commit button.
        service.add_element(train_payload_5)
        classes = service.get_page_analysis(pet_clinic_form)

        # Assert.
        assert len(classes_before['pageTitles']) == 1
        assert len(classes_before['labelCandidates']) == 0
        assert len(classes_before['commits']) == 0
        assert len(classes_before['errorMessages']) == 0
        assert len(classes_before['cancels']) == 0

        assert len(classes['pageTitles']) == 1
        assert len(classes['labelCandidates']) == 5
        assert len(classes['commits']) == 1
        assert len(classes['errorMessages']) == 4
        assert len(classes['cancels']) == 0
