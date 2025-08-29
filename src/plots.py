import math

from utils import (
    append_img_urls,
    append_row_col_for_fighter_selector,
    format_attribute_name,
    get_correlations_df,
    get_fighter_attributes_df,
    get_fighter_lookup_table,
    get_valid_attributes,
)

DEFAULT_BAR_CHART_ATTRIBUTE = 'weight'
DEFAULT_SCATTER_PLOT_ATTRIBUTE_1 = 'fastfall_speed'
DEFAULT_SCATTER_PLOT_ATTRIBUTE_2 = 'run_speed'
DEFAULT_FIGHTER_1 = '01'  # Mario
DEFAULT_FIGHTER_2 = '09'  # Luigi


def get_scatter_plot(
    var_1,
    var_2,
    screen_width,
    screen_height,
    excluded_fighter_ids,
    selected_game,
    image_size_multiplier=1.0,
    maintain_square_aspect=True,
):
    if var_1 is None:
        var_1 = DEFAULT_SCATTER_PLOT_ATTRIBUTE_1
    if var_2 is None:
        var_2 = DEFAULT_SCATTER_PLOT_ATTRIBUTE_2

    plot_height, plot_width, image_size = get_scatter_plot_sizes(
        screen_width, screen_height, maintain_square_aspect
    )
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


def get_scatter_plot_sizes(screen_width, screen_height, maintain_square_aspect=True):
    if screen_width > 992:
        # On lg screens (>992px), plot is in a column taking up ~75% of screen
        available_width = int(screen_width * 0.74) - 150
    else:
        # On smaller screens, use full width minus padding
        available_width = int(screen_width * 0.99) - 150

    # Account for header, footer, margins, card padding, plot title, etc.
    available_height = int(screen_height * 0.99) - 260

    min_width = 300
    max_width = 1400
    plot_width = min(max(available_width, min_width), max_width)

    min_height = 500
    max_height = 800
    plot_height = min(max(available_height, min_height), max_height)

    if maintain_square_aspect:
        # maintain 1:1 aspect ratio
        plot_size = min(plot_width, plot_height)
        plot_width = plot_height = plot_size

    max_image_size = 40
    min_image_size = 15
    image_size = int(min(plot_width, plot_height) / 14)
    image_size = min(image_size, max_image_size)
    image_size = max(image_size, min_image_size)

    return plot_height, plot_width, image_size


def get_corr_matrix_plot(var_1, var_2, screen_width):
    correlations_df = get_correlations_df()

    var_1 = format_attribute_name(var_1)
    var_2 = format_attribute_name(var_2)

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
        {'field': var, 'type': 'quantitative'},
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
        {'field': var, 'type': 'quantitative'},
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
    fighter_df = append_img_urls(fighter_df, game=selected_game)
    fighter_df['excluded'] = fighter_df.index.isin(excluded_fighter_ids)

    n_rows, n_cols = fighter_df[['row_number', 'col_number']].max() + 1

    plot_width = 275
    image_size = min(plot_width // n_cols, 40)  # width and height of each fighter head
    plot_height = image_size * n_rows if n_rows > 2 else image_size

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
            'height': image_size,
            'width': image_size,
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


def get_comparison_plot(
    fighter_1, fighter_2, selected_game='ultimate', screen_width=900, normalization='none'
):
    if fighter_1 is None:
        fighter_1 = DEFAULT_FIGHTER_1
    if fighter_2 is None:
        fighter_2 = DEFAULT_FIGHTER_2
    if normalization is None:
        normalization = 'none'

    plot_height, plot_width, image_size = get_comparison_plot_sizes(screen_width)

    # Retrieve the data needed for the comparison plot
    fighter_df = get_fighter_attributes_df(
        game=selected_game, normalization=normalization
    )
    plot_df = fighter_df[fighter_df['fighter_number'].isin([fighter_1, fighter_2])]
    valid_attributes = get_valid_attributes(data_type='continuous', game=selected_game)
    if '05' in [fighter_1, fighter_2] and selected_game == '64':
        # If Yoshi is selected in Smash 64, exclude shield size
        # since he has no shield size value in that game.
        # https://www.nintendo.co.jp/n01/n64/software/nus_p_nalj/smash/M_AbilityAll.html
        valid_attributes.remove('shield_size')
    plot_df = plot_df[['fighter', 'img_url', 'fighter_number', *valid_attributes]]
    plot_df = plot_df.dropna()

    # Also get raw data for dual tooltips if using normalized data
    raw_fighter_df = get_fighter_attributes_df(game=selected_game, normalization='none')
    raw_plot_df = raw_fighter_df[
        raw_fighter_df['fighter_number'].isin([fighter_1, fighter_2])
    ]
    raw_plot_df = raw_plot_df[['fighter', 'img_url', 'fighter_number', *valid_attributes]]
    raw_plot_df = raw_plot_df.dropna()

    # Transform data from wide to long format for the bar chart
    comparison_data = [
        {
            'fighter': row['fighter'],
            'fighter_number': row['fighter_number'],
            'img_url': row['img_url'],
            'attribute': attribute,
            'attribute_display': format_attribute_name(attribute),
            'value': row[attribute],
            'color': '#5B9BD5' if row['fighter_number'] == fighter_1 else '#FF8C42',
            # Add raw value for dual tooltips
            'raw_value': raw_plot_df[
                raw_plot_df['fighter_number'] == row['fighter_number']
            ][attribute].iloc[0],
        }
        for _, row in plot_df.iterrows()
        for attribute in valid_attributes
    ]

    value_title = 'Value' if normalization == 'none' else f'Value ({normalization})'

    # Main comparison bars
    comparison_bar_chart = {
        'height': plot_height,
        'width': plot_width,
        'mark': {'type': 'bar', 'opacity': 0.8},
        'encoding': {
            'tooltip': [
                {'field': 'fighter', 'type': 'nominal'},
                {'field': 'attribute_display', 'type': 'nominal', 'title': 'Attribute'},
                {
                    'field': 'value',
                    'type': 'quantitative',
                    'title': value_title,
                    'format': '.2f' if normalization != 'none' else None,
                },
                {'field': 'raw_value', 'type': 'quantitative', 'title': 'Raw Value'}
                if normalization != 'none'
                else None,
            ],
            'y': {
                'field': 'attribute_display',
                'type': 'nominal',
                'title': 'Attribute',
                'sort': {'field': 'value', 'op': 'mean', 'order': 'descending'},
                'axis': {'labelFontSize': 11},
            },
            'x': {
                'field': 'value',
                'type': 'quantitative',
                'title': value_title,
                'scale': {
                    'zero': True,
                    'domain': [0, 1] if normalization == 'minmax' else None,
                },
            },
            'color': {
                'field': 'color',
                'type': 'nominal',
                'scale': None,  # The colors are specified directly in the data
                'legend': None,  # We'll create a custom legend below
            },
            'yOffset': {'field': 'fighter', 'type': 'nominal'},
        },
        'data': {'values': comparison_data},
    }

    # Add reference line for normalized data
    baseline_x_values = {'minmax': 0.5, 'zscore': 0}
    if normalization in baseline_x_values:
        reference_line = {
            'height': plot_height,
            'width': plot_width,
            'mark': {
                'type': 'rule',
                'color': 'gray',
                'strokeDash': [3, 3],
                'opacity': 0.7,
            },
            'encoding': {'x': {'datum': baseline_x_values[normalization]}},
            'data': {'values': [{}]},
        }
        comparison_bar_chart = {
            'height': plot_height,
            'width': plot_width,
            'layer': [comparison_bar_chart, reference_line],
        }

    # Create fighter info for legend with images
    fighter_info = []
    if fighter_1 == fighter_2:
        # Single fighter case - just show one fighter centered
        fighter_row = plot_df[['fighter', 'img_url', 'fighter_number']].iloc[0]
        fighter_info.append(
            {
                'fighter': fighter_row['fighter'],
                'img_url': fighter_row['img_url'],
                'x_position': plot_width / 2,
                'color': '#5B9BD5',
            }
        )
    else:
        # Two different fighters - show both with "vs." in between
        for _, fighter_row in plot_df[
            ['fighter', 'img_url', 'fighter_number']
        ].iterrows():
            is_fighter_1 = fighter_row['fighter_number'] == fighter_1
            x_offset = -100 if is_fighter_1 else 100

            fighter_info.append(
                {
                    'fighter': fighter_row['fighter'],
                    'img_url': fighter_row['img_url'],
                    'x_position': plot_width / 2 + x_offset,
                    'color': '#5B9BD5' if is_fighter_1 else '#FF8C42',
                }
            )

        # Add "vs." image in the middle
        fighter_info.append(
            {
                'fighter': '',
                'img_url': 'assets/img/vs.png',
                'x_position': plot_width / 2,
            }
        )

    # Fighter head images for legend
    fighter_images = {
        'width': plot_width,
        'height': 0,
        'mark': {'type': 'image', 'height': image_size, 'width': image_size},
        'encoding': {
            'url': {'field': 'img_url', 'type': 'nominal'},
            'x': {
                'field': 'x_position',
                'type': 'quantitative',
                'axis': None,
                'scale': {'domain': [0, plot_width]},
            },
        },
        'data': {'values': fighter_info},
    }

    # Fighter name labels for legend
    fighter_labels = {
        'width': plot_width,
        'height': 0,
        'mark': {'type': 'text', 'fontSize': 14, 'fontWeight': 'bold'},
        'encoding': {
            'text': {'field': 'fighter', 'type': 'nominal'},
            'x': {
                'field': 'x_position',
                'type': 'quantitative',
                'axis': None,
                'scale': {'domain': [0, plot_width]},
            },
            'color': {'field': 'color', 'type': 'nominal', 'scale': None},
        },
        'data': {'values': fighter_info},
    }

    # Vega-Lite specification with vertical concatenation
    return {
        '$schema': 'https://vega.github.io/schema/vega-lite/v5.15.1.json',
        'config': {
            'axis': {'labelFontSize': 12, 'titleFontSize': 14},
            'view': {'continuousHeight': 300, 'continuousWidth': 300, 'strokeOpacity': 0},
        },
        'vconcat': [
            fighter_images,
            fighter_labels,
            comparison_bar_chart,
        ],
    }


def get_comparison_plot_sizes(screen_width):
    if screen_width >= 992:
        plot_width = int(screen_width * 0.45)
        plot_height = int(plot_width * 0.75)
        image_size = 45
    else:
        plot_width = int(screen_width * 0.55)
        plot_height = int(plot_width * 0.85)
        image_size = 40

    return plot_height, plot_width, image_size
