from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, HoverTool, Legend
from bokeh.palettes import Spectral6, Dark2, inferno
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.models import Range1d
import datetime
import itertools
import math

def top_food_plot(df_top_foods):

    foods = [i for i in df_top_foods.index]
    source = ColumnDataSource(data={
        'foods':foods,
        'calories':df_top_foods['calories'],
        'percentage':df_top_foods['% of total calories']
    })


    p = figure(
        x_range=foods, 
        plot_height=600,
        plot_width=850,
        title="Foods logged 2019-11-24 to 2019-12-24",
        y_axis_label='% of total calories'
    )

    p.vbar(
        x='foods', 
        top='percentage', 
        width=0.9, 
        source=source, 
        line_color='white', 
        fill_color=factor_cmap(
            'foods', 
            palette=inferno(df_top_foods.shape[0]), 
            factors=foods)
    )

    p.xgrid.grid_line_color = None
    p.legend.orientation = "horizontal"
    p.add_tools(HoverTool(
        tooltips=[
            ("Food", "@foods"),
            ("Total cals", "@percentage %")
        ]
    ))
    p.xaxis.major_label_orientation = math.pi/2
    show(p)
    

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
    
    
def plot_ts(df_plot, 
            ys, 
            hover_vars=None,
            date_col='dateOfSleep', 
            styles=['-o'],
            palette=['#154ba6', '#3f8dff', '#7ec4ff', '#e73360'],
            bar_width=[24*60*60*5000],
            title=None,
            plot_height=400,
            plot_width=1000,
            ylabel=None,
            xlabel=None,
            legend_location='bottom_left',
            legend_orientation='horizontal'
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
    
    for y, color, style, width in zip(ys, itertools.cycle(palette), itertools.cycle(styles), itertools.cycle(bar_width)):
        plot_dict[y] = []
        
        if style == "--":
            plot_dict[y].append(p.line(
                x=date_col,
                y=y,
                line_dash="4 4",
                color=color, 
                source=cds
            ))    
            
        if ('-' in style) and (style != '--'):
            plot_dict[y].append(p.line(
                x=date_col,
                y=y, 
                color=color, 
                source=cds
            ))
            
        if ("o" in style) or ("*" in style):
            plot_dict[y].append(p.circle(
                x=date_col,
                y=y, 
                color=color,
                alpha=0.5,
                source=cds
            ))
            
        if ("|" in style):
            plot_dict[y].append(p.vbar(
                x=date_col,
                top=y,
                fill_color=color,
                width=width,
                alpha=0.5,
                source=cds
            ))
            
        #p.add_tools(HoverTool(renderers=[plot_dict[y]], mode='hline'))
    
    legend = Legend(items=[(var, plots) for var, plots in plot_dict.items()])
    p.add_layout(legend)
    p.legend.click_policy = 'hide'
    p.legend.location = legend_location
    p.legend.orientation = legend_orientation
    
    hovers = [(y, f'@{y}') for y in ys] + [['Date', '@date']]
    
    if hover_vars is not None:
        hovers += [[h, f'@{h}'] for h in hover_vars]
        
    p.add_tools(HoverTool(tooltips=hovers))
    
    p.yaxis.axis_label = ylabel
    p.xaxis.axis_label = xlabel
    return p
