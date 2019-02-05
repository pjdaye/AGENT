import json
import os
import shutil
from distutils.dir_util import copy_tree
from unittest.mock import Mock

from boddle import boddle

from controllers.page_analysis_controller import PageAnalysisController
from services.page_analysis_service import PageAnalysisService


class TestPageAnalysisController:
    BASE_PATH = None
    BACKUP_PATH = None

    @classmethod
    def setup_class(cls):
        cls.BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
        cls.BACKUP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'backup2'))
        copy_tree(cls.BASE_PATH, cls.BACKUP_PATH)

    @classmethod
    def teardown_class(cls):
        copy_tree(cls.BACKUP_PATH, cls.BASE_PATH)
        shutil.rmtree(cls.BACKUP_PATH)

    def setup_method(self):
        class BottleAppStub:
            def __init__(self):
                self.routes = []

            # noinspection PyUnusedLocal
            def route(self, route, method, callback):
                self.routes.append((route, method))

        self.app_stub = BottleAppStub()

    def test_add_routes(self):
        # Arrange.
        controller = PageAnalysisController(self.app_stub, Mock())

        # Act.
        controller.add_routes()

        # Assert.
        assert ('/v1/status', 'GET') in self.app_stub.routes
        assert ('/v1/pageAnalysis/state/concrete', 'POST') in self.app_stub.routes
        assert ('/v1/pageTitleAnalysis/state/concrete', 'POST') in self.app_stub.routes
        assert ('/v1/pageAnalysis/state/add', 'POST') in self.app_stub.routes

    def test_get_status(self):
        # Arrange.
        controller = PageAnalysisController(self.app_stub, Mock())

        # Act.
        response = controller.get_status()

        # Assert.
        assert response.status_code == 200
        assert 'status' in response.body
        assert response.body['status'] == 'OK'

    def test_page_analysis(self):
        # Arrange.
        controller = PageAnalysisController(self.app_stub,
                                            PageAnalysisService(base_path=TestPageAnalysisController.BASE_PATH))

        with open('json/login_page.json') as file:
            login_page_concrete_state = json.loads(file.read())

        # Act.
        with boddle(json=login_page_concrete_state):
            response = controller.page_analysis()

        # Assert.
        assert response.status_code == 200
        assert 'analysis' in response.body

        classes = response.body['analysis']
        assert len(classes['pageTitles']) == 1
        assert len(classes['labelCandidates']) == 2
        assert len(classes['commits']) == 0
        assert len(classes['errorMessages']) == 0
        assert len(classes['cancels']) == 0

    def test_get_page_titles(self):
        # Arrange.
        controller = PageAnalysisController(self.app_stub,
                                            PageAnalysisService(base_path=TestPageAnalysisController.BASE_PATH))

        with open('json/login_page.json') as file:
            login_page_concrete_state = json.loads(file.read())

        # Act.
        with boddle(json=login_page_concrete_state):
            response = controller.get_page_titles()

        # Assert.
        assert response.status_code == 200
        assert 'analysis' in response.body

        classes = response.body['analysis']
        assert len(classes['pageTitles']) == 1

    def test_add(self):
        # Arrange.
        service_mock = Mock()
        controller = PageAnalysisController(self.app_stub, service=service_mock)

        json_payload = {'test': 'x'}

        # Act.
        with boddle(json=json_payload):
            response = controller.add()

        args, kwargs = service_mock.add_element.call_args

        # Assert.
        assert 'test' in args[0]
        assert args[0]['test'] == 'x'

        assert response.status_code == 200
        assert response.body == {}
