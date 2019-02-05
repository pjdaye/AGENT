from unittest.mock import patch

from abstraction.state_abstracter import StateAbstracter


@patch(StateAbstracter.__module__ + '.StateAbstracter.get_actions', side_effect=[['click'], ['set'], []])
@patch(StateAbstracter.__module__ + '.StateAbstracter.build_selector',
       side_effect=['selector_1', 'selector_2', 'selector_4'])
def test_process(build_selector_mock, get_actions_mock):
    # Arrange
    concrete_state = {
        'widgets': {
            'key_1': {
                'key': 'key_1',
                'properties': {
                    'tagName': 'A'
                }
            },
            'key_2': {
                'key': 'key_2',
                'properties': {
                    'tagName': 'INPUT'
                }
            },
            'key_3': {
                'key': 'key_3',
                'properties': {
                    'tagName': 'SOMETHING'
                }
            },
            'key_4': {
                'key': 'key_4',
                'properties': {
                    'tagName': 'INPUT'
                }
            },
        }
    }
    state_abstracter = StateAbstracter()

    # Act
    result = state_abstracter.process(concrete_state)

    # Assert
    assert len(result.widgets) == 2
    assert result.widgets[0]['selector'] == 'selector_1'
    assert result.widgets[1]['selector'] == 'selector_2'
    assert len(result.static_widgets) == 1
    assert result.static_widgets[0]['key'] == 'key_3'
    assert build_selector_mock.call_count == 3
    assert get_actions_mock.call_count == 3
    assert result.hash != 0


def test_build_selector_does_not_yet_exist():
    # Arrange
    widget = {
        'properties': {
            'tagName': 'tag_name'
        }
    }
    selectors = {

    }

    # Act
    result = StateAbstracter.build_selector(widget, selectors)

    # Assert
    assert selectors['tag_name'] == 0
    assert result == 'tag_name:visible:eq(0)'


def test_build_selector_does_already_exist():
    # Arrange
    widget = {
        'properties': {
            'tagName': 'tag_name'
        }
    }
    selectors = {
        'tag_name': 0
    }

    # Act
    result = StateAbstracter.build_selector(widget, selectors)

    # Assert
    assert selectors['tag_name'] == 1
    assert result == 'tag_name:visible:eq(1)'


def test_build_selector_widget_has_id():
    # Arrange
    widget = {
        'properties': {
            'tagName': 'tag_name',
            'id': 'id_1'
        }
    }
    selectors = {
    }

    # Act
    result = StateAbstracter.build_selector(widget, selectors)

    # Assert
    assert selectors["tag_name[id='id_1']"] == 0
    assert result == "tag_name[id='id_1']:visible:eq(0)"


def test_build_selector_widget_has_href():
    # Arrange
    widget = {
        'properties': {
            'tagName': 'tag_name',
            'href': 'href_1'
        }
    }
    selectors = {
    }

    # Act
    result = StateAbstracter.build_selector(widget, selectors)

    # Assert
    assert selectors["tag_name[href='href_1']"] == 0
    assert result == "tag_name[href='href_1']:visible:eq(0)"


def test_build_selector_widget_has_id_and_href():
    # Arrange
    widget = {
        'properties': {
            'tagName': 'tag_name',
            'id': 'id_1',
            'href': 'href_1'
        }
    }
    selectors = {
    }

    # Act
    result = StateAbstracter.build_selector(widget, selectors)

    # Assert
    assert selectors["tag_name[id='id_1'][href='href_1']"] == 0
    assert result == "tag_name[id='id_1'][href='href_1']:visible:eq(0)"


def test_get_actions_a():
    # Arrange
    widget = {
        'properties': {
            'tagName': 'A'
        }
    }

    # Act
    actions = StateAbstracter.get_actions(widget)

    # Assert
    assert actions[0] == 'click'


def test_get_actions_input():
    # Arrange
    widget = {
        'properties': {
            'tagName': 'INPUT'
        }
    }

    # Act
    actions = StateAbstracter.get_actions(widget)

    # Assert
    assert actions[0] == 'set'


def test_get_actions_button():
    # Arrange
    widget = {
        'properties': {
            'tagName': 'BUTTON'
        }
    }

    # Act
    actions = StateAbstracter.get_actions(widget)

    # Assert
    assert actions[0] == 'click'


def test_get_actions_something():
    # Arrange
    widget = {
        'properties': {
            'tagName': 'SOMETHING'
        }
    }

    # Act
    actions = StateAbstracter.get_actions(widget)

    # Assert
    assert len(actions) == 0
