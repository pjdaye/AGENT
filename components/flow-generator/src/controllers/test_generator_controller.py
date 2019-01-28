import bottle
from aist_common.log import get_logger
from bottle import request
from services.test_generator_service import TestGeneratorService

LOGGER = get_logger('test_generator_controller')


class TestGeneratorController:
    def __init__(self, app):
        self._app = app
        self._service = TestGeneratorService()

    def add_routes(self):
        self._app.route('/v1/status', method="GET", callback=self.get_status)
        self._app.route('/v1/predict', method="POST", callback=self.predict)

    @staticmethod
    def get_status():
        return bottle.HTTPResponse(body={'status': 'OK'}, status=200)

    def predict(self):
        results = {}

        query = request.json

        generated = self._service.predict(query, 1)

        generated = self.remove_consecutive_dupes(generated)

        LOGGER.info('Generation completed...')

        results["sequences"] = generated

        LOGGER.info('Results built...')

        return bottle.HTTPResponse(body=results, status=200)

    @staticmethod
    def remove_consecutive_dupes(generated):
        output = []
        for seq in generated:
            new_seq = []
            for i in range(len(seq)):
                curr = seq[i]
                if i > 0:
                    prev = seq[i - 1]
                if i == 0:
                    new_seq.append(curr)
                else:
                    if curr == prev:
                        continue
                    new_seq.append(curr)
            output.append(new_seq)
        return output
