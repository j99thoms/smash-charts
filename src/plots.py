import math

import altair as alt

from utils import format_attribute_name, get_correlations_df, get_fighter_attributes_df

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
        data_type='continuous',
        excluded_fighter_ids=excluded_fighter_ids,
        game=selected_game,
    )
    if var_2 == var_1:
        plot_df = plot_df[['fighter', 'img_url', var_1]]
    else:
        plot_df = plot_df[['fighter', 'img_url', var_1, var_2]]
    plot_df = plot_df.dropna()

    # Altair shorthand for encoding specification:
    var_1_spec = f'{var_1}:Q'
    var_2_spec = f'{var_2}:Q'

    # Create the scatter plot
    plot = (
        alt.Chart(plot_df)
        .encode(
            alt.X(var_1_spec, title=format_attribute_name(var_1)).scale(zero=False),
            alt.Y(var_2_spec, title=format_attribute_name(var_2)).scale(zero=False),
            alt.Tooltip(['fighter:N', var_1_spec, var_2_spec]),
            alt.Url('img_url:N'),
        )
        .mark_image(
            height=image_size,
            width=image_size,
        )
        .properties(
            height=plot_height,
            width=plot_width,
        )
        .configure_axis(
            titleFontSize=axis_title_size,
            labelFontSize=axis_label_size,
        )
        .interactive()
    )

    return plot


def get_scatter_plot_title(var_1, var_2):
    if var_1 is None:
        var_1 = DEFAULT_SCATTER_PLOT_ATTRIBUTE_1
    if var_2 is None:
        var_2 = DEFAULT_SCATTER_PLOT_ATTRIBUTE_2

    title = f'{format_attribute_name(var_1)} vs. {format_attribute_name(var_2)}'

    return title


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
    selected_attributes_label_red_color = alt.condition(
        f"datum.value == '{var_1}' || datum.value == '{var_2}'",
        alt.value('red'),
        alt.value('black'),
    )
    selected_attributes_label_bold_font = alt.condition(
        f"datum.value == '{var_1}' || datum.value == '{var_2}'",
        alt.value('bold'),
        alt.value('normal'),
    )

    # Create the base canvas for the correlation plot
    base_plot = (
        alt.Chart(correlations_df)
        .encode(
            alt.X('Attribute 1:N').axis(
                title=None,
                labelAngle=-45,
                labelColor=selected_attributes_label_red_color,
                labelFontWeight=selected_attributes_label_bold_font,
            ),
            alt.Y('Attribute 2:N', axis=alt.Axis(title=None))
            .axis(
                title=None,
                labelColor=selected_attributes_label_red_color,
                labelFontWeight=selected_attributes_label_bold_font,
            )
            .scale(reverse=True),
        )
        .properties(
            height=plot_height,
            width=plot_width,
        )
    )

    # For the two selected attributes being plotted on the scatter plot,
    # highlight their circles on the correlation plot by giving their outline
    # a thicker stroke width and a dashed stroke.
    selected_attributes_circle_thick_stroke = alt.condition(
        (
            f"datum['Attribute 1'] == '{var_1}' && datum['Attribute 2'] == '{var_2}'"
            '||'
            f"datum['Attribute 2'] == '{var_1}' && datum['Attribute 1'] == '{var_2}'"
        ),
        alt.value(3),
        alt.value(1),
    )

    # Add the circles to the base canvas for the correlation plot
    circles = base_plot.encode(
        alt.Color('Correlation:Q')
        .legend(orient='top')
        .scale(
            domain=[-1, 1],
            scheme='redblue',
        ),
        alt.Tooltip(['Attribute 1', 'Attribute 2', 'Correlation']),
        strokeWidth=selected_attributes_circle_thick_stroke,
    ).mark_circle(
        size=circle_size,
        stroke='black',
    )

    # If the circle size is > 900, display each correlation with 2 decimals.
    # Otherwise, only use 1 decimal for each correlation,
    # so that the text fits in the circle.
    if circle_size > 900:
        corr_text = 'corr_2dec'
    else:
        corr_text = 'corr_1dec'

    # Add the text to the base canvas for the correlation plot
    text = base_plot.encode(
        alt.Text(corr_text),
        alt.Tooltip(['Attribute 1', 'Attribute 2', 'Correlation']),
    ).mark_text(
        # Smaller circle --> smaller font size
        fontSize=get_corr_text_size(circle_size),
    )

    # Overlay the text plot on top of the circles plot
    # so that the text appears inside the circles.
    plot = (
        (circles + text)
        .configure_axis(
            grid=False,
        )
        .configure_view(
            stroke=None,
        )
        .configure_axis(
            labelFontSize=axis_label_size,
        )
    )

    return plot


def get_corr_matrix_plot_font_sizes(plot_width):
    max_axis_label_size = 16
    min_axis_label_size = 10
    axis_label_size = int(plot_width / 26)
    axis_label_size = min(axis_label_size, max_axis_label_size)
    axis_label_size = max(axis_label_size, min_axis_label_size)

    return axis_label_size


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

    sorted_df = plot_df.sort_values(by=var, ascending=False)
    sorted_fighter_list = sorted_df.fighter.to_list()
    max_val = sorted_df[var].to_list()[0] if len(plot_df.index) > 0 else 0

    # Altair shorthand for encoding spec
    var_spec = f'{var}:Q'

    # Create the base canvas for the bar chart
    base_plot = alt.Chart(plot_df).encode(
        alt.X('fighter:N', sort=sorted_fighter_list, title=None, axis=None),
        alt.Tooltip(['fighter:N', var_spec]),
    )

    # Add the bars to the base canvas for the bar chart
    bars = base_plot.mark_bar(opacity=0.7).encode(
        alt.Y(var_spec, title=format_attribute_name(var))
        .axis(
            orient='left',
            titlePadding=0,
        )
        .scale(
            domainMax=max_val * 1.15,
        ),
    )

    # Add the fighter icons to the base canvas for the bar chart
    icons = base_plot.mark_image(
        height=image_size,
        width=image_size,
    ).encode(
        alt.X(
            'fighter:N',
            sort=sorted_fighter_list,
            title='fighter',
        ).axis(
            domainOpacity=0,
            ticks=False,
            labels=False,
            titlePadding=-10,
        ),
        alt.Url('img_url:N'),
    )

    # Configure the size of the chart
    bars = bars.properties(height=plot_height, width=plot_width)
    icons = icons.properties(width=plot_width)

    # Fighter icons appear below each bar
    plot = alt.vconcat(bars, icons)

    axis_title_size, axis_label_size = get_bar_chart_font_sizes(plot_width)

    return (
        plot.configure_concat(spacing=image_size - 32)
        .configure_axis(labelFontSize=axis_label_size, titleFontSize=axis_title_size)
        .configure_view(strokeOpacity=0)
    )


def get_vertical_bar_chart(var, screen_width, plot_df):
    plot_height, plot_width, image_size = get_vertical_bar_chart_sizes(screen_width)

    sorted_df = plot_df.sort_values(by=var, ascending=False)
    sorted_fighter_list = sorted_df.fighter.to_list()
    max_val = sorted_df[var].to_list()[0] if len(plot_df.index) > 0 else 0

    # Altair shorthand for encoding spec
    var_spec = f'{var}:Q'

    # Create the base canvas for the bar chart
    base_plot = alt.Chart(plot_df).encode(
        alt.Y('fighter:N', title=None, sort=sorted_fighter_list, axis=None),
        alt.Tooltip(['fighter:N', var_spec]),
    )

    # Add the bars to the base canvas for the bar chart
    bars = base_plot.mark_bar(opacity=0.7).encode(
        alt.X(var_spec, title=format_attribute_name(var))
        .axis(
            orient='bottom',
            titlePadding=2,
        )
        .scale(
            domainMax=max_val * 1.15,
        ),
    )

    # Add the fighter icons to the base canvas for the bar chart
    icons = base_plot.mark_image(
        height=image_size,
        width=image_size,
    ).encode(
        alt.Y(
            'fighter:N',
            sort=sorted_fighter_list,
            title='fighter',
        ).axis(
            domainOpacity=0,
            ticks=False,
            labels=False,
            titlePadding=-10,
        ),
        alt.Url('img_url:N'),
    )

    # Configure the size of the chart
    bars = bars.properties(height=plot_height, width=plot_width)
    icons = icons.properties(height=plot_height)

    # Fighter icons appear to the left of each bar
    plot = alt.hconcat(icons, bars).configure_concat(spacing=image_size - 32)

    axis_title_size, axis_label_size = get_bar_chart_font_sizes(plot_width)

    return (
        plot.configure_concat(spacing=image_size - 32)
        .configure_axis(labelFontSize=axis_label_size, titleFontSize=axis_title_size)
        .configure_view(strokeOpacity=0)
    )


def get_bar_chart_title(var):
    if var is None:
        var = DEFAULT_BAR_CHART_ATTRIBUTE

    title = f'Distribution of {format_attribute_name(var)}s'

    return title


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
    fighter_df = get_fighter_attributes_df(game=selected_game)
    fighter_df['excluded'] = fighter_df.index.isin(excluded_fighter_ids)

    fighter_selector = alt.selection_point(
        name='fighter_selector',
        toggle='true',
        empty=False,
        clear=False,
        # Setting a default value is a hack to deal with unexpected behaviour when
        # the selector is empty... Conveniently, this is *also* a hack to force the
        # chart to update by incrementing said default value. Two for the price of one!
        value=cache_breaker,
    )

    n_rows, n_cols = fighter_df[['row_number', 'col_number']].max()

    plot_height = plot_width = 270
    plot = (
        alt.Chart(fighter_df)
        .encode(
            alt.X('col_number:Q', axis=None),
            alt.Y('row_number:Q', axis=None).scale(reverse=True),
            alt.Url('img_url:N'),
            alt.Tooltip(field='fighter', title=None),
            opacity=alt.condition(
                # fighter_selector XOR datum.excluded
                (fighter_selector | alt.datum.excluded)
                & ~(fighter_selector & alt.datum.excluded),
                alt.value(0.25),
                alt.value(1),
            ),
        )
        .mark_image(
            width=plot_width // n_cols,
            height=plot_height // n_rows,
        )
        .configure_view(
            strokeOpacity=0,
        )
        .properties(
            width=plot_width,
            height=plot_height,
        )
        .add_params(fighter_selector)
    )

    return plot
