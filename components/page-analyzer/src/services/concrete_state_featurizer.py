import math
import re

import numpy as np
import pandas as pd
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import sRGBColor, LabColor

from aist_common.log import get_logger

LOGGER = get_logger('concrete_state_featurizer')

color_re = re.compile(r'(rgb|rgba)\(([0-9]+?), ([0-9]+?), ([0-9]+?)([,)])')

base_colors = [
    ('black', np.array([0, 0, 0])),
    ('white', np.array([255, 255, 255])),
    ('red', np.array([255, 0, 0])),
    ('blue', np.array([0, 0, 255])),
    ('grey', np.array([128, 128, 128])),
    ('yellow', np.array([255, 255, 0])),
    ('orange', np.array([255, 165, 0])),
    ('green', np.array([0, 255, 0])),
    ('purple', np.array([128, 0, 128])),
]

basic_html_tags = ['html', 'head', 'title', 'body', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br', 'hr',
                   'b', 'blockquote', 'cite', 'code', 'i', 'pre', 'small', 'strong', 'u',
                   'form', 'input', 'textarea', 'button', 'select', 'optgroup', 'option', 'label', 'fieldset',
                   'img', 'a',
                   'ul', 'ol', 'li',
                   'table', 'th', 'tr', 'td', 'thead', 'tbody',
                   'div', 'span',
                   '#text']

basic_input_tags = ['input', 'textarea', 'select', 'option']


def calc_color_distance(rgb1, rgb2):
    color1_rgb = sRGBColor(rgb1[0], rgb1[1], rgb1[2])
    color2_rgb = sRGBColor(rgb2[0], rgb2[1], rgb2[2])

    color1_lab = convert_color(color1_rgb, LabColor)
    color2_lab = convert_color(color2_rgb, LabColor)

    delta_e = delta_e_cie2000(color1_lab, color2_lab)
    return delta_e


def calc_point_distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def get_nearest_color(color):
    result = color_re.match(color)
    if result is not None and len(result.groups()) == 5:
        color_red = int(result.groups()[1])
        color_green = int(result.groups()[2])
        color_blue = int(result.groups()[3])
        color_actual = np.array([color_red, color_green, color_blue])

        nearest_color = None
        best_distance = 99999.99
        for candidate_color in base_colors:
            color_class = candidate_color[0]
            color_rgb = candidate_color[1]
            color_distance = calc_color_distance(color_actual, color_rgb)
            if color_distance < best_distance:
                best_distance = color_distance
                nearest_color = color_class
    else:
        nearest_color = base_colors[0][0]

    return nearest_color


def normalize(df, excludes):
    result = df.copy()
    for feature_name in df.columns:
        if feature_name in excludes:
            continue
        try:
            max_value = df[feature_name].max()
            min_value = df[feature_name].min()
            if max_value == min_value:
                min_value = 0
            result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
            result[feature_name] = result[feature_name].apply(lambda x: round(abs(x), 4))
        except:
            LOGGER.error(f'Error normalizing feature: {feature_name}')
            raise RuntimeError(f'Error normalizing feature: {feature_name}')
    return result


class ConcreteStateFeaturize:

    @staticmethod
    def convert_to_feature_frame(concrete_state, measure_color_distance=True):
        data = []

        parent_map = {}
        sibling_map = {}
        input_widgets = []

        for widget in concrete_state['widgets'].values():
            parent_key = widget['key']
            children = widget['children']
            for child in children:
                parent_map[child] = parent_key
                sibling_map[child] = len(children)

            tag = widget['properties']['tagName'].lower()

            if tag in basic_input_tags:
                input_widgets.append(widget)

        for widget in concrete_state['widgets'].values():
            if widget['properties']['is-hidden']:
                continue

            key = widget['key']
            depth = widget['domLevel']
            tag = widget['properties']['tagName'].lower()

            if tag not in basic_html_tags:
                tag = 0

            if key in parent_map:
                parent_key = parent_map[key]
                parent_tag = concrete_state['widgets'][parent_key]['properties']['tagName'].lower()

                if parent_tag not in basic_html_tags:
                    parent_tag = 0

                number_of_siblings = sibling_map[key]
            else:
                parent_tag = 0
                number_of_siblings = 0

            number_of_children = len(widget['children'])

            x_percent = 0
            y_percent = 0
            font_size = 0
            font_weight = 0
            attr_for = False

            if 'properties' in widget:
                widget_props = widget['properties']

                if 'xPercent' in widget_props:
                    x_percent = int(widget_props['xPercent'])

                if 'yPercent' in widget_props:
                    y_percent = int(widget_props['yPercent'])

                if 'fontSize' in widget_props:
                    font_size = int(widget_props['fontSize'])

                if 'font-weight' in widget_props:
                    font_weight = int(widget_props['font-weight'])

                if 'for' in widget_props:
                    attr_for = widget['properties']['for']
                    if attr_for.strip() != "":
                        attr_for = True
                    else:
                        attr_for = False

            text = widget['properties']['text']

            LOGGER.debug(f'convert_feature_to_frame, {key}, {text}')
            text = text.strip()
            text = text.replace('\"', "")
            is_text = text != ""

            color = widget['properties']['color']
            bg_color = widget['properties']['background-color']

            if measure_color_distance:
                nearest_color = get_nearest_color(color)
                nearest_bg_color = get_nearest_color(bg_color)
            else:
                nearest_color = base_colors[0][0]
                nearest_bg_color = base_colors[0][0]

            # This is affected by zoom level.
            distance_from_input_widget = 9999

            for input_widget in input_widgets:
                ix, iy = int(input_widget['properties']['x']), int(input_widget['properties']['y'])
                tx, ty = int(float(widget['properties']['x'])), int(float(widget['properties']['y']))
                dist = calc_point_distance(tx, ty, ix, iy)
                if dist < distance_from_input_widget:
                    distance_from_input_widget = dist

            if attr_for:
                attr_for = 1.0
            else:
                attr_for = 0.0

            if is_text:
                is_text = 1.0
            else:
                is_text = 0.0

            for i in range(len(basic_html_tags)):
                if tag == basic_html_tags[i]:
                    tag = i + 1
                if parent_tag == basic_html_tags[i]:
                    parent_tag = i + 1

            data_row = [
                key,
                tag,
                parent_tag,
                attr_for,
                number_of_children,
                number_of_siblings,
                depth,
                x_percent,
                y_percent,
                font_size,
                font_weight,
                is_text,
                nearest_color,
                nearest_bg_color,
                distance_from_input_widget,
                text
            ]

            data.append(data_row)

        df = pd.DataFrame(data=data,
                          columns=['Key', 'Tag', 'Parent_Tag', 'Attr_For', 'Num_Children', 'Num_Siblings', 'Depth',
                                   'X_Percent', 'Y_Percent', 'Font_Size', 'Font_Weight', 'Is_Text',
                                   'Nearest_Color', 'Nearest_Bg_Color', 'Distance_From_Input', 'Text'])

        # Normalize.
        df = normalize(df, ['Key', 'Tag', 'Parent_Tag', 'Attr_For', 'Is_Text', 'Text', 'Class', 'Nearest_Color',
                            'Nearest_Bg_Color'])

        return df
