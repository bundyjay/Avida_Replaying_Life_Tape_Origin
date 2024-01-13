"""
Perform the ANOVA and estimated variance components analyses.

function:: def make_ANOVAandVariance_trajectory_dict() -> str

1. Run make_ANOVAandVariance_trajectory_dict().
2. Save the analysis dict as a csv.
3. Save the Adaptation, Chance, and History (ACH) dict as a csv.
4. Import the analysis csv and sort it.
5. Import the ACH csv and sort it.
6. Print 'Date, time, and year: date_time_year
          Module: module_path
          Saved dataframe: analysis_dataframe_location
          Saved dataframe: ACH_dataframe_location'
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import Polygon

import patchworklib as pw 
from plotnine import *
from plotnine.data import *
# import seaborn as sns
# sns.set_theme()
# pw.overwrite_axisgrid() #Overwrite Grid class provided by seaborn.

import collections
import decimal

from collections import namedtuple, defaultdict
from csv import writer
from decimal import Decimal
from dfply import arrange, group_by, mask, mutate, select, summarize, X
from math import sqrt as sqrt
from matplotlib.font_manager import FontProperties
from mizani.formatters import currency_format
from numpy import log10 as log10, std as std
from pandas import DataFrame, read_csv
from pandas.api.types import CategoricalDtype
import pandas as pd
from pathlib import Path
from plotnine import *
from scipy import stats as stats
from sys import path
from time import asctime, localtime
from time import time as t_time

module_path = Path(__file__).resolve()
analysis_folder = module_path.parent
scripts_folder = analysis_folder.parent
operations_folder = str(scripts_folder) + '/operations'
project_folder = scripts_folder.parent
output_folder = str(project_folder) + '/output_analysis'
path.insert(0, str(operations_folder))
path.insert(0, str(scripts_folder))

from fixed_precision import fixed_precision as fixed_precision

font_path = str(project_folder) + '/resources/fonts/Arial-Unicode-Regular.ttf'             
plot_title_properties = FontProperties(fname=font_path, size=14)
axis_title_properties = FontProperties(fname=font_path, size=14)
legend_title_properties = FontProperties(fname=font_path, size=14)
strip_text_properties = FontProperties(fname=font_path, size=14)
text_properties = FontProperties(fname=font_path, size=12)

"""
Establish a list of keys for the dictionaries we'll be using.
"""
keys = []
ACH_keys = []

"""
Establish some default dicts we'll add the data to later
"""
analysis_trajectory_data_dict = defaultdict(dict)
ACH_estimate_trajectory_dict = defaultdict(dict)

phase1_corr_dataframe_name = 'phase1_corr_fitness_genome_length_dataframe.csv'
corr_data = read_csv(
    output_folder 
    + '/' 
    + phase1_corr_dataframe_name
    )

times = (time for time in range(1000, 501000, 1000))

corr_dict = defaultdict(dict)
for time in times:
    key = time
    corr_dict[time] = time
    filtered_corr_data = corr_data >> mask (X.time == time)
    result = stats.linregress(filtered_corr_data['genome_length_average_value_log10'], filtered_corr_data['fitness_average_value_log10'])
    corr_dict[time] = {'slope': result[0], 'intercept': result[1], 'rvalue': result[2], 'pvalue': result[3], 'stderr': result[4], 'intercept_stderr': result.intercept_stderr}
csv_name = 'corr_by_time.csv'
file_location = output_folder + '/raw/' + csv_name

with open(file_location, 'w+', newline='') as csv_file:
    csv_writer = writer(csv_file, delimiter=',')
    csv_writer.writerow([
        'time',
        'slope',
        'intercept',
        'rvalue',
        'pvalue',
        'stderr',
        'intercept_std_error'
    ])
    
    for key in corr_dict.keys():
        values = corr_dict[key].values()
        csv_writer.writerow([key, *values])
        
raw_df = read_csv(
    file_location
    )

df = (raw_df
     >>arrange(X.time))


slope_time_plot = (ggplot(
    data=df,
    mapping=aes(
        x='time',
        y='slope'
    ))
    +geom_line(color='black')
#     +geom_line(data=df,
#                mapping=aes(x='time',
#                            y='pvalue'),
#         #        linetype='dashed',
#                color='red'
#                )
#     +geom_vline(xintercept=20000)
#     +geom_vline(xintercept=500000)
#     +geom_blank(
#         data=frame_data, 
#         mapping=aes(y='value'), 
#         inherit_aes=False
#         )
    +scale_x_continuous(
            name='Time (updates x 1000)', 
            breaks=[0, 100000, 200000, 300000, 400000, 500000],
            labels=['0', '100', '200', '300', '400', '500']
            )
    + scale_y_continuous(
            name='Slope', 
        #     breaks=[-0.5,0,0.5,1],
            labels = fixed_precision
            )
    + theme(
            figure_size=(5.2, 4.375),
            legend_title_align= 'center',
            text=element_text(fontproperties=text_properties),
            title=element_text(
                    margin= {'b': 20}, 
                    fontproperties=plot_title_properties),
            legend_position= 'none', 
            plot_background=element_rect(fill='white'),
            axis_text_x=element_text(
                    margin={'t':6}, 
                    color='black', 
                    fontproperties=text_properties),
            axis_text_y=element_text(
                    margin={'r':6}, 
                    color='black', 
                    fontproperties=text_properties),
            axis_title_x=element_blank(), 
            axis_title_y=element_blank(),
        #     axis_title_x=element_text(
        #             margin= {'t': 12}, 
        #             fontproperties=axis_title_properties), 
        #     axis_title_y=element_text(
        #             margin= {'r': 12}, 
        #             fontproperties=axis_title_properties),
            axis_ticks_major_x=element_blank(),
            axis_ticks_major_y=element_blank(),
            rect=element_rect(
                    color='white', 
                    size=3, 
                    fill='white'),
            panel_grid_major_y=element_line(
                    linetype='solid', 
                    color='gray', 
                    size=.5),
            strip_text_x = element_text(
                    fontproperties=strip_text_properties)
    ))


# Generate fake data for framing.
trait_names = ["pvalue", "pvalue"] 
value = [-.1, 1]
frame_nums = {'trait': trait_names, 'value': value}  
frame_data = DataFrame(frame_nums) 


corr_time_plot = (ggplot(
    data=df,
    mapping=aes(
        x='time',
        y='rvalue'
    ))
    +geom_line(color='black')
    +geom_line(data=df,
               mapping=aes(x='time',
                           y='pvalue'),
        #        linetype='dashed',
               color='red'
               )
    +geom_hline(yintercept=0.05)
#     +geom_vline(xintercept=20000)
#     +geom_vline(xintercept=500000)
    +geom_blank(
        data=frame_data, 
        mapping=aes(y='value'), 
        inherit_aes=False
        )
    +scale_x_continuous(
            name='Time (updates x 1000)', 
            breaks=[0, 100000, 200000, 300000, 400000, 500000],
            labels=['0', '100', '200', '300', '400', '500']
            )
    + scale_y_continuous(
            name='Pearson\'s r', 
            breaks=[-0.5,0,0.5,1],
            limits=[-0.5, 1],
            labels = fixed_precision)
    + theme(
            figure_size=(5.2, 4.375),
            legend_title_align= 'center',
            text=element_text(fontproperties=text_properties),
            title=element_text(
                    margin= {'b': 20}, 
                    fontproperties=plot_title_properties),
            legend_position= 'none', 
            plot_background=element_rect(fill='white'),
            axis_text_x=element_text(
                    margin={'t':6}, 
                    color='black', 
                    fontproperties=text_properties),
            axis_text_y=element_text(
                    margin={'r':6}, 
                    color='black', 
                    fontproperties=text_properties),
            axis_title_x=element_blank(), 
            axis_title_y=element_blank(),
        #     axis_title_x=element_text(
        #             margin= {'t': 24}, 
        #             fontproperties=axis_title_properties), 
        #     axis_title_y=element_text(
        #             margin= {'r': 12}, 
        #             fontproperties=axis_title_properties),
            axis_ticks_major_x=element_blank(),
            axis_ticks_major_y=element_blank(),
            rect=element_rect(
                    color='white', 
                    size=3, 
                    fill='white'),
            panel_grid_major_y=element_line(
                    linetype='solid', 
                    color='gray', 
                    size=.5),
            strip_text_x = element_text(
                    fontproperties=strip_text_properties
                    )
    ))

g1 = slope_time_plot
g2 = corr_time_plot 

g1 = pw.load_ggplot(g1)
g2 = pw.load_ggplot(g2)


# g1 = pw.load_ggplot(g1, figsize=(3,3))
# g2 = pw.load_ggplot(g2, figsize=(3,3))

g12= (g1)/g2
g12.savefig(fname= output_folder 
                + '/masked/phase1_plot/combined_corr_analysis_plots.tif',
                format= 'tif'
                )

# plot_name = 'comb_corr_time_plot.tif'
# corr_time_plot.save(filename=plot_name, path=output_folder +'/masked/corr_analysis_plots') 