import math

import altair as alt

from utils import (
    append_img_urls,
    append_row_col_for_fighter_selector,
    format_attribute_name,
    get_correlations_df,
    get_fighter_attributes_df,
    get_fighter_lookup_table,
)

DEFAULT_BAR_CHART_ATTRIBUTE = 'weight'
DEFAULT_SCATTER_PLOT_ATTRIBUTE_1 = 'fastfall_speed'
DEFAULT_SCATTER_PLOT_ATTRIBUTE_2 = 'run_speed'


def get_scatter_plot(
    var_1,
    var_2,
    screen_width,
    excluded_fighter_ids,
    selected_game,
    image_size_multiplier=1.0,
):
    if var_1 is None:
        var_1 = DEFAULT_SCATTER_PLOT_ATTRIBUTE_1
    if var_2 is None:
        var_2 = DEFAULT_SCATTER_PLOT_ATTRIBUTE_2

    plot_height, plot_width, image_size = get_scatter_plot_sizes(screen_width)
    axis_title_size, axis_label_size = get_scatter_plot_font_sizes(plot_width)
    image_size = image_size * image_size_multiplier

    # Retrieve the data needed for the scatter plot
    plot_df = get_fighter_attributes_df(
        excluded_fighter_ids=excluded_fighter_ids,
        game=selected_game,
    )
    if var_2 == var_1:
        plot_df = plot_df[['fighter', 'img_url', var_1]]
    else:
        plot_df = plot_df[['fighter', 'img_url', var_1, var_2]]
    plot_df = plot_df.dropna()

    # Vega-Lite specification
    return {
        '$schema': 'https://vega.github.io/schema/vega-lite/v5.15.1.json',
        'height': plot_height,
        'width': plot_width,
        'config': {
            'axis': {'labelFontSize': axis_label_size, 'titleFontSize': axis_title_size},
            'view': {'continuousHeight': 300, 'continuousWidth': 300},
        },
        'mark': {'type': 'image', 'height': image_size, 'width': image_size},
        'encoding': {
            'tooltip': [
                {'field': 'fighter', 'type': 'nominal'},
                {'field': var_1, 'type': 'quantitative'},
                {'field': var_2, 'type': 'quantitative'},
            ],
            'url': {'field': 'img_url', 'type': 'nominal'},
            'x': {
                'field': var_1,
                'scale': {'zero': False},
                'title': format_attribute_name(var_1),
                'type': 'quantitative',
            },
            'y': {
                'field': var_2,
                'scale': {'zero': False},
                'title': format_attribute_name(var_2),
                'type': 'quantitative',
            },
        },
        'params': [
            {
                'bind': 'scales',
                'name': 'interactive',
                'select': {'encodings': ['x', 'y'], 'type': 'interval'},
            }
        ],
        'data': {'values': plot_df.to_dict(orient='records')},
    }


def get_scatter_plot_title(var_1, var_2):
    if var_1 is None:
        var_1 = DEFAULT_SCATTER_PLOT_ATTRIBUTE_1
    if var_2 is None:
        var_2 = DEFAULT_SCATTER_PLOT_ATTRIBUTE_2

    return f'{format_attribute_name(var_1)} vs. {format_attribute_name(var_2)}'


def get_scatter_plot_font_sizes(plot_width):
    max_axis_title_size = 20
    min_axis_title_size = 12
    axis_title_size = int(plot_width / 19)
    axis_title_size = min(axis_title_size, max_axis_title_size)
    axis_title_size = max(axis_title_size, min_axis_title_size)

    max_axis_label_size = 16
    min_axis_label_size = 10
    axis_label_size = int(plot_width / 24)
    axis_label_size = min(axis_label_size, max_axis_label_size)
    axis_label_size = max(axis_label_size, min_axis_label_size)

    return axis_title_size, axis_label_size


def get_scatter_plot_sizes(screen_width):
    if screen_width > 1200:
        plot_width = int(screen_width / 2.8)
    elif screen_width > 900:
        plot_width = int(screen_width / 3.2)
    elif screen_width > 650:
        plot_width = int(screen_width / 3.6)
    elif screen_width > 450:
        plot_width = int(screen_width / 4.0)
    else:
        plot_width = int(screen_width / 4.5)

    plot_height = plot_width

    max_image_size = 40
    min_image_size = 15
    image_size = int(plot_width / 14)
    image_size = min(image_size, max_image_size)
    image_size = max(image_size, min_image_size)

    return plot_height, plot_width, image_size


def get_corr_matrix_plot(var_1, var_2, screen_width):
    correlations_df = get_correlations_df()

    num_attributes = len(correlations_df) ** (1 / 2)
    plot_height, plot_width, circle_size = get_corr_matrix_plot_sizes(
        screen_width,
        num_attributes,
    )
    axis_label_size = get_corr_matrix_plot_font_sizes(plot_width)

    # For the two selected attributes being plotted on the scatter plot,
    # highlight their labels on the correlation plot by giving them
    # red color and bold font.
    selected_attributes_label_red_color = {
        'condition': {
            'test': f"datum.value == '{var_1}' || datum.value == '{var_2}'",
            'value': 'red',
        },
        'value': 'black',
    }
    selected_attributes_label_bold_font = {
        'condition': {
            'test': f"datum.value == '{var_1}' || datum.value == '{var_2}'",
            'value': 'bold',
        },
        'value': 'normal',
    }

    tooltip = [
        {'field': 'Attribute 1', 'type': 'nominal'},
        {'field': 'Attribute 2', 'type': 'nominal'},
        {'field': 'Correlation', 'type': 'quantitative'},
    ]

    circles_layer = {
        'mark': {'size': circle_size, 'stroke': 'black', 'type': 'circle'},
        'encoding': {
            'tooltip': tooltip,
            'color': {
                'field': 'Correlation',
                'legend': {'orient': 'top'},
                'scale': {'domain': [-1, 1], 'scheme': 'redblue'},
                'type': 'quantitative',
            },
            'x': {
                'axis': {
                    'labelAngle': -45,
                    'labelColor': selected_attributes_label_red_color,
                    'labelFontWeight': selected_attributes_label_bold_font,
                    'title': None,
                },
                'field': 'Attribute 1',
                'type': 'nominal',
            },
            'y': {
                'axis': {
                    'labelColor': selected_attributes_label_red_color,
                    'labelFontWeight': selected_attributes_label_bold_font,
                    'title': None,
                },
                'field': 'Attribute 2',
                'scale': {'reverse': True},
                'type': 'nominal',
            },
            'strokeWidth': {
                # For the two selected attributes being plotted on the scatter plot,
                # highlight their circles on the correlation plot by giving their outline
                # a thicker stroke width.
                'condition': {
                    'test': f"datum['Attribute 1'] == '{var_1}'"
                    ' && '
                    f"datum['Attribute 2'] == '{var_2}'"
                    '||'
                    f"datum['Attribute 1'] == '{var_2}'"
                    ' && '
                    f"datum['Attribute 2'] == '{var_1}'",
                    'value': 3,
                },
                'value': 1,
            },
        },
    }

    # If circle size is > 900, display each correlation with 2 decimals.
    # Otherwise, only use 1 decimal for each correlation,
    # so that the text fits in the circle.
    corr_text = 'corr_2dec' if circle_size > 900 else 'corr_1dec'

    text_layer = {
        # Smaller circle --> smaller font size
        'mark': {'fontSize': get_corr_text_size(circle_size), 'type': 'text'},
        'encoding': {
            'tooltip': tooltip,
            'text': {'field': corr_text, 'type': 'quantitative'},
            'x': {
                'axis': {
                    'labelAngle': -45,
                    'labelColor': selected_attributes_label_red_color,
                    'labelFontWeight': selected_attributes_label_bold_font,
                    'title': None,
                },
                'field': 'Attribute 1',
                'type': 'nominal',
            },
            'y': {
                'axis': {
                    'labelColor': selected_attributes_label_red_color,
                    'labelFontWeight': selected_attributes_label_bold_font,
                    'title': None,
                },
                'field': 'Attribute 2',
                'scale': {'reverse': True},
                'type': 'nominal',
            },
        },
    }

    # Vega-Lite specification
    return {
        '$schema': 'https://vega.github.io/schema/vega-lite/v5.15.1.json',
        'height': plot_height,
        'width': plot_width,
        'config': {
            'axis': {'grid': False, 'labelFontSize': axis_label_size},
            'view': {'continuousHeight': 300, 'continuousWidth': 300},
        },
        'layer': [circles_layer, text_layer],
        'data': {'values': correlations_df.to_dict(orient='records')},
    }


def get_corr_matrix_plot_font_sizes(plot_width):
    axis_label_size = int(plot_width / 26)

    # Clamp and return:
    max_axis_label_size = 16
    min_axis_label_size = 10
    return max(min(axis_label_size, max_axis_label_size), min_axis_label_size)


def get_corr_matrix_plot_sizes(screen_width, num_attributes):
    if screen_width > 1200:
        plot_width = int(screen_width / 3.2)
    elif screen_width > 900:
        plot_width = int(screen_width / 3.6)
    elif screen_width > 650:
        plot_width = int(screen_width / 4.0)
    elif screen_width > 450:
        plot_width = int(screen_width / 4.4)
    else:
        plot_width = int(screen_width / 4.5)

    plot_height = plot_width

    circle_diameter = plot_width / num_attributes
    circle_radius = circle_diameter / 2
    circle_size = int(math.pi * (circle_radius**2))

    return plot_height, plot_width, circle_size


def get_corr_text_size(circle_size):
    # Smaller circle --> smaller font size
    if circle_size > 600:
        return 11
    if circle_size > 500:
        return 10
    if circle_size > 400:
        return 9
    if circle_size > 300:
        return 8
    if circle_size > 250:
        return 7
    # If the circle size is <= 250, don't display any text inside the circle
    return 0


def get_bar_chart(var, screen_width, excluded_fighter_ids, selected_game):
    if var is None:
        var = DEFAULT_BAR_CHART_ATTRIBUTE

    # Retrieve the data needed for the bar chart
    plot_df = get_fighter_attributes_df(
        excluded_fighter_ids=excluded_fighter_ids,
        game=selected_game,
    )
    plot_df = plot_df[['fighter', 'img_url', var]]
    plot_df = plot_df.dropna()

    return (
        get_horizontal_bar_chart(var, screen_width, plot_df)
        if screen_width > 900
        else get_vertical_bar_chart(var, screen_width, plot_df)
    )


def get_horizontal_bar_chart(var, screen_width, plot_df):
    plot_height, plot_width, image_size = get_horizontal_bar_chart_sizes(screen_width)
    axis_title_size, axis_label_size = get_bar_chart_font_sizes(plot_width)

    sorted_df = plot_df.sort_values(by=var, ascending=False)
    sorted_fighter_list = sorted_df.fighter.to_list()
    max_val = sorted_df[var].to_list()[0] if len(plot_df.index) > 0 else 0

    tooltip = [
        {'field': 'fighter', 'type': 'nominal'},
        {'field': 'weight', 'type': 'quantitative'},
    ]

    bars = {
        'height': plot_height,
        'width': plot_width,
        'mark': {'opacity': 0.7, 'type': 'bar'},
        'encoding': {
            'tooltip': tooltip,
            'x': {
                'axis': None,
                'field': 'fighter',
                'sort': sorted_fighter_list,
                'title': None,
                'type': 'nominal',
            },
            'y': {
                'axis': {'orient': 'left', 'titlePadding': 0},
                'field': var,
                'scale': {'domainMax': max_val * 1.15},
                'title': format_attribute_name(var),
                'type': 'quantitative',
            },
        },
    }

    icons = {
        'width': plot_width,
        'mark': {'type': 'image', 'height': image_size, 'width': image_size},
        'encoding': {
            'tooltip': tooltip,
            'url': {'field': 'img_url', 'type': 'nominal'},
            'x': {
                'axis': {
                    'domainOpacity': 0,
                    'labels': False,
                    'ticks': False,
                    'titlePadding': -10,
                },
                'field': 'fighter',
                'sort': sorted_fighter_list,
                'title': 'Fighter',
                'type': 'nominal',
            },
        },
    }

    # Vega-Lite specification
    return {
        '$schema': 'https://vega.github.io/schema/vega-lite/v5.15.1.json',
        'config': {
            'axis': {'labelFontSize': axis_label_size, 'titleFontSize': axis_title_size},
            'concat': {'spacing': image_size - 32},
            'view': {'continuousHeight': 300, 'continuousWidth': 300, 'strokeOpacity': 0},
        },
        'vconcat': [bars, icons],  # Fighter icons appear below each bar
        'data': {'values': plot_df.to_dict(orient='records')},
    }


def get_vertical_bar_chart(var, screen_width, plot_df):
    plot_height, plot_width, image_size = get_vertical_bar_chart_sizes(screen_width)
    axis_title_size, axis_label_size = get_bar_chart_font_sizes(plot_width)

    sorted_df = plot_df.sort_values(by=var, ascending=False)
    sorted_fighter_list = sorted_df.fighter.to_list()
    max_val = sorted_df[var].to_list()[0] if len(plot_df.index) > 0 else 0

    tooltip = [
        {'field': 'fighter', 'type': 'nominal'},
        {'field': 'weight', 'type': 'quantitative'},
    ]

    bars = {
        'height': plot_height,
        'width': plot_width,
        'mark': {'opacity': 0.7, 'type': 'bar'},
        'encoding': {
            'tooltip': tooltip,
            'y': {
                'axis': None,
                'field': 'fighter',
                'sort': sorted_fighter_list,
                'title': None,
                'type': 'nominal',
            },
            'x': {
                'axis': {'orient': 'bottom', 'titlePadding': 2},
                'field': var,
                'scale': {'domainMax': max_val * 1.15},
                'title': format_attribute_name(var),
                'type': 'quantitative',
            },
        },
    }

    icons = {
        'height': plot_height,
        'mark': {'type': 'image', 'height': image_size, 'width': image_size},
        'encoding': {
            'tooltip': tooltip,
            'url': {'field': 'img_url', 'type': 'nominal'},
            'y': {
                'axis': {
                    'domainOpacity': 0,
                    'labels': False,
                    'ticks': False,
                    'titlePadding': -10,
                },
                'field': 'fighter',
                'sort': sorted_fighter_list,
                'title': 'Fighter',
                'type': 'nominal',
            },
        },
    }

    # Vega-Lite specification
    return {
        '$schema': 'https://vega.github.io/schema/vega-lite/v5.15.1.json',
        'config': {
            'axis': {'labelFontSize': axis_label_size, 'titleFontSize': axis_title_size},
            'concat': {'spacing': image_size - 32},
            'view': {'continuousHeight': 300, 'continuousWidth': 300, 'strokeOpacity': 0},
        },
        'hconcat': [icons, bars],  # Fighter icons appear to the left of each bar
        'data': {'values': plot_df.to_dict(orient='records')},
    }


def get_bar_chart_title(var):
    if var is None:
        var = DEFAULT_BAR_CHART_ATTRIBUTE

    return f'Distribution of {format_attribute_name(var)}s'


def get_bar_chart_font_sizes(plot_width):
    max_axis_title_size = 20
    min_axis_title_size = 12
    axis_title_size = int(plot_width / 50)
    axis_title_size = min(axis_title_size, max_axis_title_size)
    axis_title_size = max(axis_title_size, min_axis_title_size)

    max_axis_label_size = 16
    min_axis_label_size = 10
    axis_label_size = int(plot_width / 60)
    axis_label_size = min(axis_label_size, max_axis_label_size)
    axis_label_size = max(axis_label_size, min_axis_label_size)

    return axis_title_size, axis_label_size


def get_horizontal_bar_chart_sizes(screen_width):
    plot_height = 250
    plot_width = int(screen_width * 0.86)  # Plot takes up 86% of the screen

    max_image_size = 24
    min_image_size = 15
    image_size = int(plot_width / 62)
    image_size = min(image_size, max_image_size)
    image_size = max(image_size, min_image_size)

    return plot_height, plot_width, image_size


def get_vertical_bar_chart_sizes(screen_width):
    plot_height = 1200
    image_size = 20

    max_plot_width = 550
    if screen_width > 550:
        plot_width = int(screen_width * 0.8)
    else:
        plot_width = int(screen_width * 0.7)
    plot_width = min(plot_width, max_plot_width)

    return plot_height, plot_width, image_size


def get_fighter_selector_chart(
    excluded_fighter_ids=None, selected_game='ultimate', cache_breaker=999
):
    if excluded_fighter_ids is None:
        excluded_fighter_ids = []

    fighter_df = get_fighter_lookup_table(game=selected_game)
    fighter_df = append_row_col_for_fighter_selector(fighter_df)
    fighter_df = append_img_urls(fighter_df)
    fighter_df['excluded'] = fighter_df.index.isin(excluded_fighter_ids)

    n_rows, n_cols = fighter_df[['row_number', 'col_number']].max()

    plot_height = plot_width = 270

    selected_fighter_test = {
        # fighter_selector XOR datum.excluded
        'and': [
            {'or': [{'param': 'fighter_selector'}, 'datum.excluded']},
            {'not': {'and': [{'param': 'fighter_selector'}, 'datum.excluded']}},
        ]
    }

    # Vega-Lite specification
    return {
        '$schema': 'https://vega.github.io/schema/vega-lite/v5.15.1.json',
        'height': plot_height,
        'width': plot_width,
        'config': {
            'view': {'continuousWidth': 300, 'continuousHeight': 300, 'strokeOpacity': 0}
        },
        'mark': {
            'type': 'image',
            'height': plot_height // n_rows,
            'width': plot_width // n_cols,
        },
        'encoding': {
            'tooltip': {'field': 'fighter', 'title': None},
            'url': {'field': 'img_url', 'type': 'nominal'},
            'x': {
                'axis': None,
                'field': 'col_number',
                'type': 'quantitative',
            },
            'y': {
                'axis': None,
                'field': 'row_number',
                'type': 'quantitative',
                'scale': {'reverse': True},
            },
            'opacity': {
                'condition': {
                    'test': selected_fighter_test,
                    'value': 0.25,
                },
                'value': 1,
            },
        },
        'params': [
            {
                'name': 'fighter_selector',
                'select': {'type': 'point', 'clear': False, 'toggle': 'true'},
                'value': cache_breaker,
            }
        ],
        'data': {'values': fighter_df.to_dict(orient='records')},
    }
