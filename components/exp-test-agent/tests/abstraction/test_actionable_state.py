from unittest.mock import patch, Mock

from abstraction.actionable_state import ActionableState


def test_add_widget():
    # Arrange
    widget = {
        'key': 'key_1'
    }
    actionable_state = ActionableState()

    # Act
    actionable_state.add_widget(widget)

    # Assert
    assert actionable_state.widget_map['key_1'] == widget
    assert len(actionable_state.widgets) == 1
    assert actionable_state.widgets[0] == widget


def test_add_static_widget():
    # Arrange
    widget = {
        'key': 'key_1'
    }
    actionable_state = ActionableState()

    # Act
    actionable_state.add_static_widget(widget)

    # Assert
    assert len(actionable_state.static_widgets) == 1
    assert actionable_state.static_widgets[0] == widget


def test_get_all_widgets():
    # Arrange
    actionable_state = ActionableState()
    actionable_state.widgets = [
        {
            'key': 'key_1',
            'label': 'label_1',
            'actions': ['set']
        },
        {
            'key': 'key_2',
            'label': 'label_2',
            'actions': []
        }
    ]
    actionable_state.static_widgets = [
        {
            'key': 'key_3',
            'label': 'label_3',
            'actions': []
        },
        {
            'key': 'key_4',
            'label': 'label_4',
            'actions': ['set']
        }
    ]

    # Act
    result = actionable_state.get_all_widgets()

    # Assert
    assert len(result) == 4
    assert result[0]['key'] == 'key_1'
    assert result[1]['key'] == 'key_2'
    assert result[2]['key'] == 'key_3'
    assert result[3]['key'] == 'key_4'


def test_find_widget_with_label_widget_exists():
    # Arrange
    actionable_state = ActionableState()
    actionable_state.widgets = [
        {
            'key': 'key_1',
            'label': 'label_1',
            'actions': ['set']
        },
        {
            'key': 'key_2',
            'label': 'label_2',
            'actions': []
        }
    ]
    actionable_state.static_widgets = [
        {
            'key': 'key_3',
            'label': 'label_3',
            'actions': []
        },
        {
            'key': 'key_4',
            'label': 'label_4',
            'actions': ['set']
        }
    ]

    # Act
    result = actionable_state.find_widget_with_label('LABEL_1', 'set')

    # Assert
    assert result['key'] == 'key_1'


def test_find_widget_with_label_label_is_none():
    # Arrange
    actionable_state = ActionableState()
    actionable_state.widgets = [
        {
            'key': 'key_1',
            'label': None,
            'actions': ['set']
        },
        {
            'key': 'key_2',
            'label': 'label_2',
            'actions': []
        }
    ]
    actionable_state.static_widgets = [
        {
            'key': 'key_3',
            'label': 'label_3',
            'actions': []
        },
        {
            'key': 'key_4',
            'label': 'label_4',
            'actions': ['set']
        }
    ]

    # Act
    result = actionable_state.find_widget_with_label('LABEL_1', 'set')

    # Assert
    assert result is None


def test_find_widget_with_label_widget_does_not_exist():
    # Arrange
    actionable_state = ActionableState()
    actionable_state.widgets = [
        {
            'key': 'key_1',
            'label': 'label',
            'actions': ['set']
        },
        {
            'key': 'key_2',
            'label': 'label_2',
            'actions': []
        }
    ]
    actionable_state.static_widgets = [
        {
            'key': 'key_3',
            'label': 'label_3',
            'actions': []
        },
        {
            'key': 'key_4',
            'label': 'label_4',
            'actions': ['set']
        }
    ]

    # Act
    result = actionable_state.find_widget_with_label('LABEL_1', 'set')

    # Assert
    assert result is None


def test_find_widget_with_label_action_does_not_match():
    # Arrange
    actionable_state = ActionableState()
    actionable_state.widgets = [
        {
            'key': 'key_1',
            'label': 'label_1',
            'actions': ['']
        },
        {
            'key': 'key_2',
            'label': 'label_2',
            'actions': []
        }
    ]
    actionable_state.static_widgets = [
        {
            'key': 'key_3',
            'label': 'label_3',
            'actions': []
        },
        {
            'key': 'key_4',
            'label': 'label_4',
            'actions': ['set']
        }
    ]

    # Act
    result = actionable_state.find_widget_with_label('LABEL_1', 'set')

    # Assert
    assert result is None


@patch(ActionableState.__module__ + '.hash')
@patch(ActionableState.__module__ + '.frozenset')
def test_calculate_hash(frozenset_mock, hash_mock):
    # Arrange
    actionable_state = ActionableState()
    actionable_state.widgets = [
        {
            'key': 'key_1',
            'label': 'label_1',
            'actions': ['']
        },
        {
            'key': 'key_2',
            'label': 'label_2',
            'actions': []
        }
    ]
    actionable_state.static_widgets = [
        {
            'key': 'key_3',
            'label': 'label_3',
            'actions': []
        },
        {
            'key': 'key_4',
            'label': 'label_4',
            'actions': ['set']
        }
    ]
    frozenset_mock_return_value = Mock()
    frozenset_mock.return_value = frozenset_mock_return_value
    hash_mock_return_value = Mock()
    hash_mock.return_value = hash_mock_return_value

    # Act
    actionable_state.calculate_hash()

    # Assert
    assert actionable_state.hash == hash_mock_return_value
    assert 'key_1' in frozenset_mock.call_args[0][0]
    assert 'key_2' in frozenset_mock.call_args[0][0]
    hash_mock.assert_called_with(frozenset_mock_return_value)
