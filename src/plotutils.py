from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, HoverTool, Legend
from bokeh.palettes import Spectral6, Dark2
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
import datetime
import itertools


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
    
    
def plot_ts(df_plot, ys, 
            date_col='dateOfSleep', 
            styles=['-o'],
            palette=['#154ba6', '#3f8dff', '#7ec4ff', '#e73360'],
            title=None,
            plot_height=400,
            plot_width=1000
           ):
    
    df_plot = df_plot.reset_index().copy()
    df_plot['date'] = df_plot[date_col].dt.strftime('%Y-%m-%d')
    cds = ColumnDataSource(data=df_plot)
    

    p = figure(
        x_axis_type="datetime",
        plot_height=plot_height,
        plot_width=plot_width,
        title=title,
    )
    
    plot_dict = {}
    
    for y, color, style in zip(ys, itertools.cycle(palette), itertools.cycle(styles)):
        plot_dict[y] = []
        
        if "-" in style:
            plot_dict[y].append(p.line(
                x='dateOfSleep',
                y=y, 
                color=color, 
                source=cds
            ))
            
        if ("o" in style) or ("*" in style):
            plot_dict[y].append(p.circle(
                x='dateOfSleep',
                y=y, 
                color=color,
                alpha=0.5,
                source=cds
            ))
    
    legend = Legend(items=[(var, plots) for var, plots in plot_dict.items()])
    p.add_layout(legend)
    p.legend.click_policy = 'hide'
    
    hovers = [(y, f'@{y}') for y in ys] + [['Date', '@date']]
    p.add_tools(HoverTool(tooltips=hovers))

    show(p)
