"""
Generate custom manual colors based on ancestor_seed. 

dict:: color_dict
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

from pathlib import Path
from sys import path

module_path = Path(__file__).resolve()
analysis_folder = module_path.parent
scripts_folder = analysis_folder.parent
operations_folder = str(scripts_folder) + '/operations'
colorspace_folder = str(scripts_folder) + '/operations/python-colorspace'
project_folder = scripts_folder.parent
output_folder = str(project_folder) + '/output_analysis'
path.insert(0, str(operations_folder))
path.insert(0, str(scripts_folder))
path.insert(0, str(colorspace_folder))

# Generate custom colors based on number of ancestor_seeds
from colorspace import qualitative_hcl
colors = qualitative_hcl("dark3").colors(10)
# print(colors)


color_dict = {
        101 : colors[0],
        102 : colors[1],
        103 : colors[2],
        104 : colors[3],
        105 : colors[4],
        106 : colors[5],
        107 : colors[6],
        108 : colors[7],
        109 : colors[8],
        110 : colors[9]
}

# color_dict = {
#         101 : '#E16A86',
#         102 : '#CB7F2F',
#         103 : '#9F9400',
#         104 : '#50A315',
#         105 : '#00AC79',
#         106 : '#00AAB7',
#         107 : '#009ADE',
#         108 : '#A87BE4',
#         109 : '#DA65C3',
#         110 : '#E16A86'
# }