import altair as alt
from utils import (
    get_character_data, get_correlations_df
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

    if var_1 is None or var_2 is None:
        # Return an empty plot and empty title
        if verbose:
            print("Empty scatter plot.")

        plot = alt.Chart().mark_point().properties(
             plot_height=plot_height,
             plot_width=plot_width
        )
        title = ""

        return plot, title
    
    if verbose:
        print(f"var_1: {var_1}")
        print(f"var_2: {var_2}")

    # Retrieve the data needed for the scatter plot
    plot_df = get_character_data()
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
    # Otherwise, only use 1 decimal for each correlation, so that the 
    # text fits in the circle.
    if circle_size > 900:
        corr_text = 'corr_text_2'
    else:
        corr_text = 'corr_text_1'
    
    # Add the text to the base canvas for the correlation plot
    text = base_plot.encode(
        alt.Text(corr_text),
        alt.Tooltip(['Attribute 1', 'Attribute 2', 'Correlation']),
    ).mark_text(
        # Smaller circle --> smaller font size
        fontSize=get_corr_text_size(circle_size)
    )

    # Overlay the text plot on top of the circles plot
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

def get_hori_bar_chart(var, screen_width, verbose=False):
    plot_height, plot_width, image_size = get_hori_bar_chart_sizes(screen_width)
    axis_title_size, axis_label_size = get_bar_chart_font_sizes(plot_width)

    if var is None:
        var = "Weight"

    if verbose:
        print("--bar_chart--")

        print(f"bar_chart_var: {var}")

        print(f"bar_chart_plot_width: {plot_width}")
        print(f"bar_chart_plot_height: {plot_height}")
        print(f"bar_chart_image_size: {image_size}")
    
        print(f"bar_chart_axis_title_size: {axis_title_size}")
        print(f"bar_chart_axis_label_size: {axis_label_size}")

    plot_df = get_character_data()
    plot_df = plot_df[['Character', 'img_url', var]]
    plot_df = plot_df.dropna()

    sorted_df = plot_df.sort_values(by=var, ascending=False)
    sorted_list = sorted_df.Character.to_list()
    max_val = sorted_df[var].to_list()[0]

    base_plot = alt.Chart(plot_df).encode(
        alt.X('Character', title=None, sort=sorted_list, axis=None),
        alt.Tooltip(['Character', var])
    )

    bars = base_plot.mark_bar(opacity=0.7).encode(
        alt.Y(var).axis(
            orient='left', titlePadding=0
        ).scale(
            domainMax = max_val * 1.15
        ),
        # alt.Color(
            # var,
            # bin=alt.Bin(maxbins=4), 
            # scale=alt.Scale(scheme='dark2'),
            # title=var
        # ),
    ).properties(
        height=plot_height,
        width=plot_width
    )
    
    pics = base_plot.encode(
        alt.X('Character', title='Character', sort=sorted_list).axis(
            domainOpacity=0, ticks=False, labels=False, titlePadding=-10
        ),
        alt.Url('img_url'),
    ).mark_image(
        height=image_size, 
        width=image_size
    ).properties(
        width=plot_width
    )

    plot = alt.vconcat(
        bars, pics
    ).configure_concat(
        spacing=-(32 - image_size) # idk lol
    ).configure_view(
        strokeOpacity=0
    ).configure_axis(
        labelFontSize=axis_label_size,
        titleFontSize=axis_title_size,
    )

    return plot

def get_vert_bar_chart(var, screen_width, verbose=False):
    plot_height, plot_width, image_size = get_vert_bar_chart_sizes(screen_width)
    axis_title_size, axis_label_size = get_bar_chart_font_sizes(plot_width)

    if var is None:
        var = "Weight"

    if verbose:
        print(f"bar_chart_var: {var}")

        print(f"bar_chart_plot_width: {plot_width}")
        print(f"bar_chart_plot_height: {plot_height}")
        print(f"bar_chart_image_size: {image_size}")
    
        print(f"bar_chart_axis_title_size: {axis_title_size}")
        print(f"bar_chart_axis_label_size: {axis_label_size}")
    
    plot_df = get_character_data()
    plot_df = plot_df[['Character', 'img_url', var]]
    plot_df = plot_df.dropna()

    sorted_df = plot_df.sort_values(by=var, ascending=False)
    sorted_list = sorted_df.Character.to_list()
    max_val = sorted_df[var].to_list()[0]

    base_plot = alt.Chart(plot_df).encode(
        alt.Y('Character', title=None, sort=sorted_list, axis=None),
        alt.Tooltip(['Character', var])
    )

    bars = base_plot.mark_bar(opacity=0.7).encode(
        alt.X(var).axis(
            orient='bottom', titlePadding=2
        ).scale(
            domainMax = max_val * 1.15
        ),
        # alt.Color(
            # var,
            # bin=alt.Bin(maxbins=4), 
            # scale=alt.Scale(scheme='dark2'),
            # title=var
        # ),
    ).properties(
        height=plot_height,
        width=plot_width
    )
    
    pics = base_plot.encode(
        alt.Y('Character', title='Character', sort=sorted_list).axis(
            domainOpacity=0, ticks=False, labels=False, titlePadding=-10
        ),
        alt.Url('img_url'),
    ).mark_image(
        height=image_size, 
        width=image_size
    ).properties(
        height=plot_height
    )

    plot = alt.hconcat(
        pics, bars
    ).configure_concat(
        spacing=-(32 - image_size) # idk lol
    ).configure_view(
        strokeOpacity=0
    ).configure_axis(
        labelFontSize=axis_label_size,
        titleFontSize=axis_title_size
    )

    return plot

def get_bar_chart_title(var):
    title = f"Distribution of {var}s"

    return title

def get_bar_chart_font_sizes(plot_width):
    MAX_AXIS_TITLE_SIZE = 20
    MIN_AXIS_TITLE_SIZE = 12

    MAX_AXIS_LABEL_SIZE = 16
    MIN_AXIS_LABEL_SIZE = 10

    axis_title_size = min(int(plot_width / 50), MAX_AXIS_TITLE_SIZE)
    axis_title_size = max(axis_title_size, MIN_AXIS_TITLE_SIZE)

    axis_label_size = min(int(plot_width / 60), MAX_AXIS_LABEL_SIZE)
    axis_label_size = max(axis_label_size, MIN_AXIS_LABEL_SIZE)

    return axis_title_size, axis_label_size

def get_hori_bar_chart_sizes(screen_width):
    PLOT_HEIGHT = 250
    MAX_IMAGE_SIZE = 24
    MIN_IMAGE_SIZE = 15

    plot_height = PLOT_HEIGHT

    plot_width = int(screen_width * 0.86)

    image_size = min(int(plot_width / 62), MAX_IMAGE_SIZE)
    image_size = max(image_size, MIN_IMAGE_SIZE)

    return plot_height, plot_width, image_size

def get_vert_bar_chart_sizes(screen_width):
    PLOT_HEIGHT = 1200
    MAX_PLOT_WIDTH = 550
    IMAGE_SIZE = 20

    plot_height = PLOT_HEIGHT

    if screen_width > 550:
        plot_width = int(screen_width * 0.8)
    else:
        plot_width = int(screen_width * 0.7)
    plot_width = min(plot_width, MAX_PLOT_WIDTH)

    image_size = IMAGE_SIZE

    return plot_height, plot_width, image_size
