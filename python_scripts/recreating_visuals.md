## Recreating the visuals from the manuscript

<p>Overview</p>

<p>
Most figures require running three scripts to recreate. The first is a script that creates the data dictionary. These scripts have "data_dict" in the title and are found in the operations folder. These folders read the raw data output by Avida and creates Python dictionaries that store the raw data from each run. The second script creates a sorted dataframe and also outputs a .csv file so the data can be reviewed. These scripts have "create_csv" in the title and are found in the operations folder. Note that each of these "create_csv" scripts has an associated "sort_csv" script that is imported to create custom sorting for each dataframe. The third script creates plots and tables. These files have unique names and are found in the analysis folder in the scripts directory.
</p>

<p>
To run a script, ensure that you are in the same directory as the script (e.g., cd operations). Then execute the script (e.g, python3 phase1.py) If you have already executed the script to create the csv for a plot (to generate a plot or table that uses the same data) then you only need to run the analysis file script. 
</p>

<p>Figs 1 & 2</p>

<p>
Figures 1 & 2 are schematics that were created in Inkscape. There are no scripts to recreate them.
</p>

<p>Fig 3</p>

<p>
data dict file: data_dict_phase1.py<br/>
create csv file: create_csv_phase1.py<br/>
analysis file: combined_genome_length_w_std.py<br/>
</p>

<p>Fig 4</p>

<p>
data dict file: data_dict_phase1.py<br/>
create csv file: create_csv_phase1.py<br/>
analysis file: combined_fitness_w_std.py<br/>
</p>

<p>Fig 5</p>

<p>
data dict file: data_dict_phase1_corr_fitness_genome_length.py<br/>
create csv file: create_csv_phase1_corr_fitness_genome_length.py<br/>
analysis file: combined_correlations.py<br/>
</p>

<p>S1 Table</p>

<p>
data dict file: data_dict_phase1_average_fitness_and_average_length.py <br/>
create csv file: create_csv_phase1_average_fitness_and_average_length.py <br/>
analysis file: phase1_average_fitness_and_average_length_analysis.py <br/>
</p>

<p>S2 Table</p>

<p>
data dict file: data_dict_phase1_corr_fitness_genome_length.py<br/>
create csv file: create_csv_phase1_corr_fitness_genome_length.py<br/>
analysis file: corr_analysis_lineage.py<br/>
</p>

<p>S1 Fig</p>

<p>
data dict file: data_dict_phase1_average_fitness_and_average_length.py <br/>
create csv file: create_csv_phase1_average_fitness_and_average_length.py <br/>
analysis file: phase1_average_fitness_and_average_length_boxplots_nocolor.py <br/>
</p>

<p>S2 Fig</p>

<p>
data dict file: data_dict_phase1_corr_fitness_genome_length.py<br/>
create csv file: create_csv_phase1_corr_fitness_genome_length.py<br/>
analysis file: comb_corr_analysis_time.py<br/>
</p>
