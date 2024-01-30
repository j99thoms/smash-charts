import altair as alt
from utils import (
    get_character_attributes_df, get_correlations_df
)

def get_scatter_plot(
    var_1,
    var_2,
    plot_height,
    plot_width,
    image_size,
    axis_title_size,
    axis_label_size,
    verbose=False
):
    if verbose:
        print("--- Updating Scatter Plot ---")
        print(f"scatter_var_1: {var_1}")
        print(f"scatter_var_2: {var_2}")

    if var_1 is None or var_2 is None:
        # Return an empty plot and empty title
        plot = alt.Chart().mark_point().properties(
             plot_height=plot_height,
             plot_width=plot_width
        )
        title = ""

        return plot, title

    # Retrieve the data needed for the scatter plot
    plot_df = get_character_attributes_df()
    if var_2 == var_1:
         plot_df = plot_df[['Character', 'img_url', var_1]]
    else:
        plot_df = plot_df[['Character', 'img_url', var_1, var_2]]
    plot_df = plot_df.dropna()
    
    # Create the scatter plot
    plot = alt.Chart(plot_df).encode(
        alt.X(var_1).scale(zero=False),
        alt.Y(var_2).scale(zero=False),
        alt.Tooltip(['Character', var_1, var_2]),
        alt.Url('img_url')
    ).mark_image(  
        height=image_size, # TODO: Image size slider??
        width=image_size
    ).properties(
        height=plot_height,
        width=plot_width
    ).configure_axis(
        titleFontSize=axis_title_size,
        labelFontSize=axis_label_size
    ).interactive()

    title = f"{var_1} vs. {var_2}"

    return plot, title

def get_corr_matrix_plot(
    var_1,
    var_2,
    plot_height,
    plot_width,
    circle_size,
    axis_label_size
):
    # Retrieve the data needed for the correlation plot
    corr_df = get_correlations_df()

    # For the two selected attributes being plotted on the scatter plot,
    # highlight their labels on the correlation plot by giving them
    # red color and bold font.
    selected_attributes_label_red_color = alt.condition(
        f"datum.value == '{var_1}' || datum.value == '{var_2}'",
        alt.value('red'),
        alt.value('black')
    )
    selected_attributes_label_bold_font = alt.condition(
        f"datum.value == '{var_1}' || datum.value == '{var_2}'",
        alt.value('bold'),
        alt.value('normal')
    )

    # Create the base canvas for the correlation plot
    base_plot = alt.Chart(corr_df).encode(
        alt.X('Attribute 1:N').axis(
            title=None,
            labelAngle=-45,
            labelColor=selected_attributes_label_red_color,
            labelFontWeight=selected_attributes_label_bold_font
        ),
        alt.Y('Attribute 2:N', axis=alt.Axis(title=None)).axis(
            title=None,
            labelColor=selected_attributes_label_red_color,
            labelFontWeight=selected_attributes_label_bold_font
        )
    ).properties(
        height=plot_height,
        width=plot_width
    )

    # For the two selected attributes being plotted on the scatter plot,
    # highlight their circles on the correlation plot by giving their outline
    # a thicker stroke width and a dashed stroke.
    selected_attributes_circle_thick_stroke = alt.condition(
        f"""
            datum['Attribute 1'] == '{var_1}' 
            && datum['Attribute 2'] == '{var_2}' 
            || 
            datum['Attribute 2'] == '{var_1}' 
            && datum['Attribute 1'] == '{var_2}'
        """,
        alt.value(3),
        alt.value(1)
    )
    selected_attributes_circle_dashed_outline = alt.condition(
            f"""
            datum['Attribute 1'] == '{var_1}' 
            && datum['Attribute 2'] == '{var_2}' 
            || 
            datum['Attribute 2'] == '{var_1}' 
            && datum['Attribute 1'] == '{var_2}'
            """,
            alt.value((2,2)),
            alt.value((1,0))
    )

    # Add the circles to the base canvas for the correlation plot
    circles = base_plot.encode(
        alt.Color('Correlation:Q').legend(orient="top").scale(
            domain=[-1, 1],
            scheme='redblue'
        ),
        alt.Tooltip(['Attribute 1', 'Attribute 2', 'Correlation']),
        strokeWidth=selected_attributes_circle_thick_stroke,
        # strokeDash=selected_attributes_circle_dashed_outline
    ).mark_circle(
        size=circle_size,
        stroke='black'
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
        fontSize=get_corr_text_size(circle_size)
    )

    # Overlay the text plot on top of the circles plot
    # so that the text appears inside the circles.
    plot = (circles + text).configure_axis(
        grid=False
    ).configure_view(
        stroke=None
    ).configure_axis(
        labelFontSize=axis_label_size
    )

    return plot

def get_corr_text_size(circle_size):
    # Smaller circle --> smaller font size
    if circle_size > 600:
        return 11
    elif circle_size > 500:
        return 10
    elif circle_size > 400:
        return 9
    elif circle_size > 300:
        return 8
    elif circle_size > 250:
        return 7
    else:
        # If the circle size is <= 250, don't display any text inside the circle
        return 0

def get_bar_chart(var, screen_width, verbose=False):
    if var is None:
        var = "Weight"

    if screen_width > 900:
        chart_orientation = "horizontal"
    else:
        chart_orientation = "vertical"
    plot_height, plot_width, image_size = get_bar_chart_sizes(
        screen_width,
        chart_orientation
    )

    if verbose:
        print("--- Updating Bar Chart ---")
        print(f"bar_chart_var: {var}")
        print(f"bar_chart_orientation: {chart_orientation}")
        print(f"bar_chart_plot_width: {plot_width}")
        print(f"bar_chart_plot_height: {plot_height}")
        print(f"bar_chart_image_size: {image_size}")

    # Retrieve the data needed for the bar chart
    plot_df = get_character_attributes_df()
    plot_df = plot_df[['Character', 'img_url', var]]
    plot_df = plot_df.dropna()

    sorted_df = plot_df.sort_values(by=var, ascending=False)
    sorted_character_list = sorted_df.Character.to_list()
    max_val = sorted_df[var].to_list()[0]

    # Create the base canvas for the bar chart
    if chart_orientation == "horizontal":
        base_plot = alt.Chart(plot_df).encode(
            alt.X('Character', sort=sorted_character_list, title=None, axis=None),
            alt.Tooltip(['Character', var])
        )
    else:
        base_plot = alt.Chart(plot_df).encode(
            alt.Y('Character', title=None, sort=sorted_character_list, axis=None),
            alt.Tooltip(['Character', var])
        )

    # Add the bars to the base canvas for the bar chart
    if chart_orientation == "horizontal":
        bars = base_plot.mark_bar(opacity=0.7).encode(
            alt.Y(var).axis(
                orient='left', titlePadding=0
            ).scale(
                domainMax = max_val * 1.15
            )
        )
    else:
        bars = base_plot.mark_bar(opacity=0.7).encode(
            alt.X(var).axis(
                orient='bottom', titlePadding=2
            ).scale(
                domainMax = max_val * 1.15
            )
        )

    # Add the character icons to the base canvas for the bar chart
    if chart_orientation == "horizontal":
        icons = base_plot.mark_image(
            height=image_size,
            width=image_size
        ).encode(
            alt.X(
                'Character',
                sort=sorted_character_list,
                title='Character'
            ).axis(
                domainOpacity=0,
                ticks=False,
                labels=False,
                titlePadding=-10
            ),
            alt.Url('img_url')
        )
    else:
        icons = base_plot.mark_image(
            height=image_size,
            width=image_size
        ).encode(
            alt.Y(
                'Character',
                sort=sorted_character_list,
                title='Character'
            ).axis(
                domainOpacity=0,
                ticks=False,
                labels=False,
                titlePadding=-10
            ),
            alt.Url('img_url')
        )

    # Configure the size of the chart
    bars = bars.properties(
        height=plot_height,
        width=plot_width
    )
    if chart_orientation == "horizontal":
        icons = icons.properties(width=plot_width)
    else:
        icons = icons.properties(height=plot_height)

    # Overlay the character icons plot on top of the bar chart plot
    if chart_orientation == "horizontal":
        # Charcter icons appear below each bar
        plot = alt.vconcat(bars, icons)
    else:
        # Charcter icons appear to the left of each bar
        plot = alt.hconcat(icons, bars)

    # Configure the plot to look nice:
    # Tight layout and appropriate axis font sizes
    axis_title_size, axis_label_size = get_bar_chart_font_sizes(plot_width)
    plot = plot.configure_concat(
        spacing=-(32 - image_size) # trial and error - it works
    ).configure_view(
        strokeOpacity=0
    ).configure_axis(
        labelFontSize=axis_label_size,
        titleFontSize=axis_title_size,
    )

    if verbose:
        print(f"bar_chart_axis_title_size: {axis_title_size}")
        print(f"bar_chart_axis_label_size: {axis_label_size}")

    return plot

def get_bar_chart_title(var):
    title = f"Distribution of {var}s"

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

def get_bar_chart_sizes(screen_width, chart_orientation):
    if chart_orientation == "horizontal":
        plot_height = 250
        plot_width = int(screen_width * 0.86) # Plot takes up 86% of the screen

        max_image_size = 24
        min_image_size = 15
        image_size = int(plot_width / 62)
        image_size = min(image_size, max_image_size)
        image_size = max(image_size, min_image_size)
    else:
        plot_height = 1200
        image_size = 20

        max_plot_width = 550
        if screen_width > 550:
            plot_width = int(screen_width * 0.8)
        else:
            plot_width = int(screen_width * 0.7)
        plot_width = min(plot_width, max_plot_width)

    return plot_height, plot_width, image_size
