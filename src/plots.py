import altair as alt
from utils import get_character_data

def get_scatter_plot(
    var_1, 
    var_2,
    plot_height, 
    plot_width,
    image_size=30, 
    axis_title_size=17, 
    axis_label_size=21
):
    if var_1 is None or var_2 is None:
         plot = alt.Chart().mark_point().properties(
             plot_height=plot_height, plot_width=plot_width)
         return plot, ""
    print(f"var_1: {var_1}")
    print(f"var_2: {var_2}")

    plot_df = get_character_data()
    if var_2 == var_1:
         plot_df = plot_df[['Character', 'img_url', var_1]]
    else:
        plot_df = plot_df[['Character', 'img_url', var_1, var_2]]
    plot_df = plot_df.dropna()
    
    plot = alt.Chart(plot_df).encode(
        alt.X(var_1, scale=alt.Scale(zero=False)),
        alt.Y(var_2, scale=alt.Scale(zero=False)),
        alt.Tooltip(['Character', var_1, var_2]),
        alt.Url('img_url')
    ).mark_image(  
        width=image_size,
        height=image_size
    ).properties(
        height=plot_height,
        width=plot_width
    )
    
    plot = plot.configure_axis(
        labelFontSize=axis_label_size,
        titleFontSize=axis_title_size
    )
    plot = plot.interactive()
    # TODO: Image size slider??

    title = f"{var_1} vs. {var_2}"

    return plot, title


def get_hori_bar_chart(var, plot_height, plot_width):
    IMAGE_SIZE = 30
    AXIS_TITLE_SIZE = 21
    AXIS_LABEL_SIZE = 15

    image_size = IMAGE_SIZE
    axis_title_size, axis_label_size = AXIS_TITLE_SIZE, AXIS_LABEL_SIZE

    if var is None:
        var = "Weight"

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
    
    ### Icons above bars ###
    # pics = base_plot.encode(
    #     alt.Y('above_bar:Q', scale=alt.Scale(domainMax = max_val * 1.15, clamp=True)),
    #     alt.Url('img_url'),
    # ).mark_image(plot_height=image_size, plot_width=image_size).transform_calculate(
    #     above_bar=f"datum.{var} + ({max} / 10)"
    # )

    # dotted_lines = base_plot.encode(
    #     alt.Y('above_bar:Q', scale=alt.Scale(domainMax = max_val * 1.15)),
    #     alt.Y2(var)
    # ).mark_line(strokeDash=(2,3), strokeWidth=2, color='black').transform_calculate(
    #     above_bar=f"datum.{var} + ({max} / 10)"
    # )
    
    # plot = bars + dotted_lines + pics
    
    # plot = plot.configure_axis(
    #     labelFontSize=15,
    #     titleFontSize=21
    # ).properties(
    #     plot_height=plot_height,
    #     plot_width=plot_width
    # )


    ### Icons as axis labels ###
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


def get_bar_chart_title(var):
    title = f"Distribution of {var}s"

    return title
