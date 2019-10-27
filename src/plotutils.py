from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Spectral6, Dark2
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
import datetime

def sleep_summary_plot(sleep_dict):

    stages = [k for k in sleep_dict.keys()]
    hours = [v for v in sleep_dict.values()]
    hhmm = [str(datetime.timedelta(seconds=v)) for v in sleep_dict.values()]

    source = ColumnDataSource(data={
        'stages':stages,
        'hours':hours,
        'hhmm':hhmm
    })


    p = figure(
        x_range=stages, 
        plot_height=250, 
        title="Fitbit Sleep Data",
    )

    p.vbar(
        x='stages', 
        top='hours', 
        width=0.9, 
        source=source, 
        legend="stages",
        line_color='white', 
        fill_color=factor_cmap(
            'stages', 
            palette=['#154ba6', '#3f8dff', '#7ec4ff', '#e73360'], 
            factors=stages)
    )

    p.xgrid.grid_line_color = None
    p.legend.orientation = "horizontal"
    p.add_tools(HoverTool(
        tooltips=[
            ("Stage", "@stages"),
            ("Duration", "@hhmm")
        ]
    ))

    show(p)