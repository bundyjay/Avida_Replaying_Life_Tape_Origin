"""
Create the data trajectory plot for Phase 1.

function:: def create_phase1_plot() -> str

This is Fig. 3.
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

import patchworklib as pw 
from plotnine import *
from plotnine.data import *
import seaborn as sns
sns.set_theme()
pw.overwrite_axisgrid() #Overwrite Grid class provided by seaborn.

from dfply import group_by, mask, select, summarize, X
from matplotlib.font_manager import FontProperties
from mizani.breaks import log_breaks, mpl_breaks
from mizani.formatters import currency_format, custom_format, mpl_format,scientific_format
from mizani.transforms import log10_trans, identity_trans
from pandas import DataFrame, read_csv
from pathlib import Path
from plotnine import (
        aes, 
        element_blank, 
        element_line, 
        element_rect, 
        element_text, 
        facet_wrap, 
        geom_blank, 
        geom_line,  
        geom_point, 
        geom_smooth, 
        geom_vline, 
        ggplot, 
        labeller,
        scale_color_manual,
        scale_size_manual,
        scale_x_continuous, 
        scale_y_continuous, 
        scale_y_log10, 
        theme)
from sys import path 
from time import asctime, localtime, time

module_path = Path(__file__).resolve()
analysis_folder = module_path.parent
scripts_folder = analysis_folder.parent
operations_folder = str(scripts_folder) + '/operations'
project_folder = scripts_folder.parent
output_folder = str(project_folder) + '/output_analysis'
path.insert(0, str(operations_folder))
path.insert(0, str(scripts_folder))

from custom_color_dict import color_dict as color_dict
from fixed_precision import fixed_precision as fixed_precision
from label_title import label_title as label_title
from revised_phase1_y_breaks_101_fitness import revised_phase1_y_breaks as revised_phase1_y_breaks
from revised_phase1_y_format_101_fitness import revised_phase1_y_format as revised_phase1_y_format

font_path = str(project_folder) + '/resources/fonts/Arial-Unicode-Regular.ttf'             
plot_title_properties = FontProperties(fname=font_path, size=20)
axis_title_properties = FontProperties(fname=font_path, size=14)
legend_title_properties = FontProperties(fname=font_path, size=20)
strip_text_properties = FontProperties(fname=font_path, size=20)
text_properties = FontProperties(fname=font_path, size=14)

phase1_dataframe = read_csv(
        str(output_folder) 
        + '/phase1_dataframe.csv') 

group_means = (phase1_dataframe 
        >> group_by(X.trait, X.time) 
        >> summarize(
        group_mean = X.evolved_population_average_value_log10.mean(),
        group_std = X.evolved_population_average_value_log10.std()) 
        >> mask (X.trait == 'fitness'))

size_dict = {
        101 : 1.5,
        102 : .5,
        103 : .5,
        104 : .5,
        105 : .5,
        106 : .5,
        107 : .5,
        108 : .5,
        109 : .5,
        110 : .5
}

def create_phase1_plot():

        """
        Create the Phase 1 plot.

        :return: 'Date, time, and year: date_time_year
                Module: module_path
                Saved image: phase1_plot_location'
        :rtype: str
        """
        
        phase1_dataframe_combined = (phase1_dataframe 
                >> select (
                        X.series, 
                        X.trait, 
                        X.time, 
                        X.ancestor_seed,  
                        X.ancestor_value, 
                        X.ancestor_value_log10, 
                        X.evolved_population_average_value, 
                        X.evolved_population_average_value_log10)        
                >> mask (
                        X.ancestor_seed == 101,
                        X.trait == 'fitness',
                        X.time <= 20000
                        ))
        
        df = phase1_dataframe_combined
     
        # Use ancestor data to plot ancestor values.
        fitness_ancestor_value =  (
                phase1_dataframe_combined.query(
                        "trait == 'fitness'")
                        # ['ancestor_value_log10']
                        ['ancestor_value']
                        .mean())
        trait_names = ["fitness"] 
        value = list([fitness_ancestor_value])
        ancestor_values = {'trait': trait_names, 'ancestor_value': value}  
        ancestor_data = DataFrame(ancestor_values) 

        # Generate fake data for framing.
        trait_names = ["fitness", "fitness"] 
        value = [0.01, 10000]
        frame_nums = {'trait': trait_names, 'value': value}  
        frame_data = DataFrame(frame_nums) 
        
        phase1_plot_101_20k = (
                ggplot(
                        data=phase1_dataframe_combined, 
                        mapping=aes(
                                x='time',
                                y='evolved_population_average_value', 
                                color= 'factor(ancestor_seed)', 
                                group= 'series'))
                + geom_line(size= .5)
                + geom_point()
                # + geom_vline(xintercept=20000)
                # + geom_vline(xintercept=100000)
                # + geom_vline(xintercept=500000)

                + geom_point(
                        data= ancestor_data, 
                        mapping=aes(
                                x=0, 
                                y='ancestor_value'
                                ), 
                        shape= '*', 
                        size= 10, 
                        inherit_aes= False)
                + geom_blank(
                        data=frame_data, 
                        mapping=aes(y='value'), 
                        inherit_aes=False)
                + scale_color_manual(values = color_dict)
                + scale_x_continuous(
                        name='Time (updates x 1000)', 
                        # labels = currency_format(
                        #         prefix='', 
                        #         suffix='', 
                        #         digits=0, 
                        #         big_mark=',')
                        labels = ['0', '5', '10', '15', '20']
                        )
                # + scale_y_log10(name='Size',
                #                 breaks=[80, 90, 100, 110, 120],
                #                 limits=[80, 120],
                #                 # labels=['0.1','1.0', '10', '100']
                #                 # breaks=revised_phase1_y_breaks,
                #                 # labels=revised_phase1_y_format
                #                 )
                + scale_y_log10(name='Log Fitness',
                                # breaks=[.01, 10, 10000, 10000000, 10000000000],
                                breaks=[.01, 1, 100, 10000, 1000000, 100000000],
                                labels=['-2','0', '2','4','6', '8' ]
                                )
                # + scale_y_log10(name='Fitness',
                #                 # breaks=[.01, 10, 10000, 10000000, 10000000000],
                #                 breaks=[.01, 1, 100, 10000, 1000000, 100000000],
                #                 labels=['10\u207B\u00B2','10\u2070', '10\u00B2','10\u2074','10\u2076', '10\u2078' ]
                #                 )
                + theme(
                        # figure_size=(5.2, 4.375),
                        # panel_spacing = .05,
                        # legend_title_align= 'center',
                        text=element_text(fontproperties=text_properties),
                        # title=element_text(
                        #         margin= {'b': 20}, 
                        #         fontproperties=plot_title_properties),
                        legend_position= 'none', 
                        plot_background=element_rect(fill='white'),
                        # axis_text_x=element_text(
                        #         margin={'t':18}, 
                        #         color='black', 
                        #         size=8, 
                        #         fontproperties=text_properties),
                        # axis_text_y=element_text(
                        #         margin={'r':6}, 
                        #         color='black', 
                        #         size=8, 
                        #         fontproperties=text_properties),
                        axis_title_x=element_blank(), 
                        axis_title_y=element_blank(),
                        # axis_title_x=element_text(
                        #         margin= {'t': 12}, 
                        #         fontproperties=axis_title_properties), 
                        # axis_title_y=element_text(
                        #         margin= {'r': 12}, 
                        #         fontproperties=axis_title_properties),
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
                        # strip_text_x = element_text(
                        #         fontproperties=strip_text_properties)
                        )
                ) 


        phase1_dataframe_combined = (phase1_dataframe 
                >> select (
                        X.series, 
                        X.trait, 
                        X.time, 
                        X.ancestor_seed,  
                        X.ancestor_value, 
                        X.ancestor_value_log10, 
                        X.evolved_population_average_value, 
                        X.evolved_population_average_value_log10)        
                >> mask (
                        X.ancestor_seed == 101,
                        X.trait == 'fitness',
                        ))
        df = phase1_dataframe_combined
       
        fitness_ancestor_value =  (
                phase1_dataframe_combined.query(
                        "trait == 'fitness'")
                        ['ancestor_value']
                        .mean())
        trait_names = ["fitness"] 
        value = list([fitness_ancestor_value])
        ancestor_values = {'trait': trait_names, 'ancestor_value': value}  
        ancestor_data = DataFrame(ancestor_values) 

        # Generate fake data for framing.
        trait_names = ["fitness", "fitness"] 
        value = [0.01, 10000]
        frame_nums = {'trait': trait_names, 'value': value}  
        frame_data = DataFrame(frame_nums) 
        
        phase1_plot_101 = (
                ggplot(
                        data=phase1_dataframe_combined, 
                        mapping=aes(
                                x='time',
                                y='evolved_population_average_value', 
                                color= 'factor(ancestor_seed)', 
                                group= 'series'))
                
                # + geom_point()
                # + geom_smooth(
                #         method='lm',
                #         color='black',
                #         # formula='y ~ poly(x, degree=2)'
                #         )
                
                + geom_line(size= 1.5)
                # + geom_vline(xintercept=20000)
                # + geom_vline(xintercept=100000)
                # + geom_vline(xintercept=500000)

                + geom_point(
                        data= ancestor_data, 
                        mapping=aes(
                                x=0, 
                                y='ancestor_value'
                                ), 
                        shape= '*', 
                        size= 10, 
                        inherit_aes= False)
                + geom_blank(
                        data=frame_data, 
                        mapping=aes(y='value'), 
                        inherit_aes=False)
                + scale_color_manual(values = color_dict)
                + scale_x_continuous(
                        name='Time (updates x 1000)', 
                        # labels = currency_format(
                        #         prefix='', 
                        #         suffix='', 
                        #         digits=0, 
                        #         big_mark=',')
                        labels = ['0', '100', '200', '300', '400', '500']
                        )
                # + scale_y_log10(name='Size',
                #                 # breaks=[95, 100, 105, 110, 115]
                #                 breaks=[80, 90, 100, 110, 120],
                #                 limits=[80, 120]
                #                 )
                # + scale_y_log10(name='Fitness',
                #                 # breaks=[.01, 10, 10000, 10000000, 10000000000],
                #                 breaks=[.01, 1, 100, 10000, 1000000, 100000000],
                #                 labels=['10\u207B\u00B2','10\u2070', '10\u00B2','10\u2074','10\u2076', '10\u2078' ]
                #                 )
                
                + scale_y_log10(name='Log Fitness',
                                # breaks=[.01, 10, 10000, 10000000, 10000000000],
                                breaks=[.01, 1, 100, 10000, 1000000, 100000000],
                                labels=['-2','0', '2','4','6', '8' ]
                                )
                + theme(
                        # figure_size=(5.2, 4.375),
                        # panel_spacing = .05,
                        # legend_title_align= 'center',
                        text=element_text(fontproperties=text_properties),
                        # title=element_text(
                        #         margin= {'b': 20}, 
                        #         fontproperties=plot_title_properties),
                        legend_position= 'none', 
                        plot_background=element_rect(fill='white'),
                        # axis_text_x=element_text(
                        #         margin={'t':18}, 
                        #         color='black', 
                        #         size=8, 
                        #         fontproperties=text_properties),
                        # axis_text_y=element_text(
                        #         margin={'r':6}, 
                        #         color='black', 
                        #         size=8, 
                        #         fontproperties=text_properties),
                        axis_title_x=element_blank(), 
                        axis_title_y=element_blank(),
                        # axis_title_x=element_text(
                        #         margin= {'t': 12}, 
                        #         fontproperties=axis_title_properties), 
                        # axis_title_y=element_text(
                        #         margin= {'r': 12}, 
                        #         fontproperties=axis_title_properties),
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
                        # strip_text_x = element_text(
                        #         fontproperties=strip_text_properties)
                        )
                )
         
        
        phase1_dataframe_combined = (phase1_dataframe 
        >> select (
                X.series, 
                X.trait, 
                X.time, 
                X.ancestor_seed,  
                X.ancestor_value, 
                X.ancestor_value_log10, 
                X.evolved_population_average_value, 
                X.evolved_population_average_value_log10)
        >> mask (X.trait == 'fitness'))
        
        grand_mean_data = (phase1_dataframe_combined
        >> group_by(X.time)
        >> summarize(grand_mean = X.evolved_population_average_value_log10.mean())
        )
        
        # print(grand_mean_data)
                
        # Use ancestor data to plot ancestor values.
        fitness_ancestor_value =  (
                phase1_dataframe_combined.query(
                        "trait == 'fitness'")
                        # ['ancestor_value_log10']
                        ['ancestor_value_log10']
                        .mean())
        # genome_length_ancestor_value =  (
        #         phase1_dataframe_combined.query(
        #                 "trait == 'genome_length'")
        #                 # ['ancestor_value_log10']
        #                 ['ancestor_value']
        #                 .mean())
        trait_names = ["fitness"] 
        value = list([fitness_ancestor_value])
        ancestor_values = {'trait': trait_names, 'ancestor_value': value}  
        ancestor_data = DataFrame(ancestor_values) 

        # Generate fake data for framing.
        trait_names = ["fitness", "fitness"] 
        # value = [0.01, 100000000]
        value = [-2, 8]
        frame_nums = {'trait': trait_names, 'value': value}  
        frame_data = DataFrame(frame_nums) 
        
        phase1_plot = (
                ggplot(
                        data=phase1_dataframe_combined, 
                        mapping=aes(
                                x='time',
                                y='evolved_population_average_value_log10', 
                                color= 'factor(ancestor_seed)',  
                                size= 'factor(ancestor_seed)',
                                group= 'series'))
                + geom_line()
                # + geom_vline(xintercept=20000)
                # + geom_vline(xintercept=100000)
                # + geom_vline(xintercept=500000)
                
                +geom_line(data=grand_mean_data,
                           color='black',
                           size=1,
                           mapping=aes(
                                   x='time',
                                   y='grand_mean'),
                           inherit_aes=False
                           )

                + geom_point(
                        data= ancestor_data, 
                        mapping=aes(
                                x=0, 
                                y='ancestor_value'
                                ), 
                        shape= '*', 
                        size= 4, 
                        inherit_aes= False)
                + geom_blank(
                        data=frame_data, 
                        mapping=aes(y='value'), 
                        inherit_aes=False)
                + scale_color_manual(values = color_dict)
                + scale_size_manual(values = size_dict)
                + scale_x_continuous(
                        name='Time (updates x 1000)', 
                        # labels = currency_format(
                        #         prefix='', 
                        #         suffix='', 
                        #         digits=0, 
                        #         big_mark=',')
                        labels = ['0', '100', '200', '300', '400', '500']
                        )
                # + scale_y_log10()
                + scale_y_continuous(name='Fitness',
                                     # breaks=[.01, 10, 10000, 10000000, 10000000000],
                                     # breaks=[.01, 1, 100, 10000, 1000000, 100000000],
                                     breaks=[-2, 0, 2, 4, 6, 8],
                                #      labels=['10\u207B\u00B2','10\u2070', '10\u00B2','10\u2074','10\u2076', '10\u2078' ]
                                     labels=['-2','0','2','4','6','8']
                                     )
                + theme(
                        figure_size=(5.2, 4.375),
                        # panel_spacing = .03,
                        legend_title_align= 'center',
                        text=element_text(fontproperties=text_properties),
                        title=element_text(fontproperties=plot_title_properties),
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
                                fontproperties=strip_text_properties),
                        )) 

        
                
        std_plot = (
                ggplot(
                        data=group_means, 
                        mapping=aes(
                                x='time',
                                y='group_std'))
                
                #     + geom_point()
                
                + geom_line()
                # + geom_vline(xintercept=20000)
                # + geom_vline(xintercept=500000)
                
                +scale_x_continuous(
                        name='Time (updates x 1,000)', 
                        breaks=[0, 100000, 200000, 300000, 400000, 500000],
                        labels=['0', '100', '200', '300', '400', '500']
                        )
                + scale_y_continuous(name='Variation in log fitness',
                                breaks=[0.0, 0.5, 1.0, 1.5, 2],
                                labels=['0.0', '0.5', '1.0', '1.5', '2.0']
                                )
                + theme(
                        figure_size=(5.2, 4.375),
                        # panel_spacing = .03,
                        legend_title_align= 'center',
                        text=element_text(fontproperties=text_properties),
                        title=element_text(fontproperties=plot_title_properties),
                        legend_position= 'none', 
                        plot_background=element_rect(fill='white'),
                        axis_text_x=element_text(
                                margin={'t':6}, 
                                color='black', 
                                # size=8, 
                                fontproperties=text_properties),
                        axis_text_y=element_text(
                                margin={'r':6}, 
                                color='black', 
                                # size=8, 
                                fontproperties=text_properties),
                        axis_title_x=element_blank(), 
                        axis_title_y=element_blank(),
                        # axis_title_x=element_text(
                        #         margin= {'t': 12}, 
                        #         fontproperties=axis_title_properties), 
                        # axis_title_y=element_text(
                        #         margin= {'r': 12}, 
                        #         fontproperties=axis_title_properties),
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
                                fontproperties=strip_text_properties),
                        )
                        )   
 
        
        g1 = phase1_plot_101_20k
        g2 = phase1_plot_101
        g3 = phase1_plot
        g4 = std_plot

        # g1 = pw.load_ggplot(g1)
        # g2 = pw.load_ggplot(g2)
        # g3 = pw.load_ggplot(g3)
        
        # g1 = pw.load_ggplot(g1, figsize=(4,4))
        # g2 = pw.load_ggplot(g2, figsize=(4,4))
        # g3 = pw.load_ggplot(g3, figsize=(8,8))

        g1 = pw.load_ggplot(g1, figsize=(3,3))
        g2 = pw.load_ggplot(g2, figsize=(3,3))
        g3 = pw.load_ggplot(g3, figsize=(3,3))
        g4 = pw.load_ggplot(g4, figsize=(3,3))
        
        g1234 = (g1|g2)/(g3|g4)
        g1234.savefig(fname= output_folder 
                        + '/masked/phase1_plot/combined_fitness_w_std.tif',
                    format= 'tif'
                        )


        # phase1_plot_name= '101_revised_phase1_genome_length_20k.tif'
        # phase1_plot.save(
        #         filename = phase1_plot_name, 
        #         path = (
        #                 output_folder 
        #                 + '/masked/phase1_plot'))

        date_time_year = asctime(localtime(time()))       
        
        return (
                '\n\n'
                'Date, time, and year: %s \n' 
                'Module: %s \n'
                'Saved image: %s' 
                % (
                date_time_year, 
                module_path, (
                        output_folder 
                        + '/masked/phase1_plot/' 
                        + 'phase1_fitness_combined')))

if __name__ == '__main__':
   print(create_phase1_plot())
  
