from services.test_generator_service import TestGeneratorService


class TestFlowGenerator:

    def test_happy_path(self):
        # Arrange.
        test_generator = TestGeneratorService()

        # Act.
        output = test_generator.predict(['observe', 'textbox'], 1)

        # Assert.
        assert output is not None
        assert len(output) > 0
        assert len(output[0]) > 0

    def test_unsupported_token(self):
        # Arrange.
        test_generator = TestGeneratorService()

        # Act.
        output = test_generator.predict(['observe', 'simple'], 1)

        # Assert.
        assert output == []
