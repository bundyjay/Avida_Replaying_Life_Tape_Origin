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

import collections
import decimal

from collections import namedtuple, defaultdict
from csv import writer
from decimal import Decimal
from dfply import arrange, group_by, mask, mutate, select, summarize, X
from math import sqrt as sqrt
from mizani.formatters import currency_format
from numpy import log10 as log10, std as std
from pandas import read_csv
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

# print(corr_data['genome_length_average_value_log10'].corr(corr_data['fitness_average_value_log10']))
# result = stats.linregress(corr_data['genome_length_average_value_log10'], corr_data['fitness_average_value_log10'])
# print(result.rvalue)

# corr_by_lineage = corr_data >> group_by(X.ancestor_seed) >> summarize(corr=X.genome_length_average_value_log10.corr(X.fitness_average_value_log10))
# corr_by_lineage = corr_data >> group_by(X.ancestor_seed) >> summarize(corr=X.genome_length_average_value_log10.corr(X.fitness_average_value_log10))
# print(corr_by_lineage)

# lineages = (seed for seed in range(101, 111))

lineages = (seed for seed in range(101, 111))
corr_dict = defaultdict(dict)
for seed in lineages:
    key = seed
    corr_dict[seed] = seed
    filtered_corr_data = corr_data >> group_by(X.ancestor_seed) >> mask (X.ancestor_seed == seed)
    result = stats.linregress(filtered_corr_data['genome_length_average_value_log10'], filtered_corr_data['fitness_average_value_log10'])
    # print(result)
    corr_dict[seed] = {'slope': round(result[0], 3), 'intercept': round(result[1], 3), 'rvalue': round(result[2], 3), 'pvalue': round(result[3], 3), 'stderr': round(result[4], 3), 'intercept_stderr': round(result.intercept_stderr, 3)}
    
    # print(filtered_corr_data)
    # print(seed)
# print(corr_dict)

csv_name = 'corr_by_lineage.csv'
file_location = output_folder + '/raw/' + csv_name

with open(file_location, 'w+', newline='') as csv_file:
    csv_writer = writer(csv_file, delimiter=',')
    csv_writer.writerow([
        'seed',
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
    file_location,
    dtype={'seed': str}
    )

df = (raw_df
     >>arrange(X.seed))

print(df)