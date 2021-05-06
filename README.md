# ABE65100_Final_Project

Project Name: Crop Selector Tool
Programmer: Steven Doyle
Date: 05.05.2021


This tool uses publicly available crop and environmental data to match suitable crops with subnational jurisdictions. 
The environmental data comes from the FAO Global Agro Ecological Zones dataset of raster files and the WorldClim dataset of 
raster files, while the plant information comes from the FAO ECOCrop dataset. The environmental csv files are produced by 
using a spatial join function in ArcGIS Desktop Pro to create a dataset where entries correspond to intersects between GADM 36 
Level 1 'states' and environmental variable values. This means that each row in an environmental csv file is a point on an evenly 
spaced coordinate grid with a corresponding state and environmental attribute value.

The 'raw_env_var_csv' folder contains the environmental csv files. The files named '*_join.csv' are raw environmental attribute 
files. These are processed first running them through the 'join_clean.py' program to remove any rows which were not successful 
spatial joins. The outputs are labeled as 'checked_*_join.csv'.

The 'check_soils_join.csv' file undergoes additional conversions through the 'soils_data_conversions.py' script, using the dictionary
 file 'SU_Info.csv' to convert the categorical soil type variable into continuous variable values which are associated with the soil 
type. It also averages the values for each soil attribute between rows of the same administrative zones and then creates a new 
dataframe from this. The output file is saved as 'processed_soil.csv'. It is noted that this file is then manually copied into the 
folder 'processed_env_files' by the user.

The other environmental variables are averaged by administrative district using the 'env_data_conversions.py' script, which repeats 
the averaging process for each environmental attribute file and saves them under the 'processed_env_files' folder as 
'processed_*.csv'.

The combined environmental variable file is created using the 'env_variables_construction.py' script to first combine all 
'processed_*.csv' files into a single table and then transform their values into versions compatible with the ECOCrop agronomic 
requirements. The output csv file is saved under the 'processed_env_files' folder as 'env_var.csv'.

The ECOCrop list is processed by first inputting the 'cropbasices_scrape.csv' file found in the 'ecocrop_files' folder into the 
'ecocrop_quality.py' script. This script selects the agronomic columns which are most important to plant growth, conducts a data 
quality check to drop any rows with na values or gross errors and reverse any swapped values, and saves the resulting dataframe in 
the same folder as 'ecocrop_cleaned.csv'.

The crop selector tool is then run using the 'ecocrop_cleaned.csv' and 'env_var.csv' files and the 'cultivation_function.py' 
script to identify crops that can be grown in a specific administrative region. It scores each crop based on how well its 
agronomic requirements align with the region's environmental attributes and returns a dataframe of the plant list including 
these values that is saved as '*_*_*_scores.csv' with the astericks corresponding to administrative region name, administrative 
region type, and country name. For demonstration of this tool, the Morogoro Region of Tanzania was chosen.

Metrics and statistics for the scores dataset are calculated using the 'metrics_and_statistics.csv.py' script. This script inputs 
the '*_*_*_scores.csv', reports a table calculating the means, standard deviations, and modes of the high scoring subset titled 
'*_pass_metrics.csv', and produces two plots. The first is a boxplot comparing the absolute minimum rainfall requirement for 
the passing subset versus the entire ECOCrop dataset saved as 'Min_Rain_Diff.png' and the second is a histogram of the maximum 
altitude of plants in the passing subset saved as 'Max_Alt.png'. It also produces three additional csv files: the full dataset 
with pass and fail scores and attributes: '*_all_data.csv', just the dataset of passing plants '*_passing_data.csv', and 
just the dataset of failing plants: '*_failing_data.csv'.

Graphical exploration is conducted using the 'morogoro_graphical_exp.py' script and taking '*_all_data.csv', '*_passing_data.csv', 
and '*_failing_data.csv' csv files as inputs. It totals the number of plants excluded by each attribute and produces a bar graph 
of this which is saved as 'Fail_Bar.png'. It also conducts a principal component fit and a principal component analysis, producing 
output files 'pca_fit.png' and 'pca_scatter.png', respectively. It uses modules scikitlearn and seaborne for these two analyses.

The ECOCrop graphical exploration used in project update 1 is found in the 'project_update_1' folder. The script 
'ecocrop_exploration.py' is used to conduct this analysis. It requires the files 'ecocrop_cleaned.csv' and 'cropbasics_scrape.csv' 
as inputs and produces a plot of the difference in rainfall probability distribution between raw and cleaned datasets, a histogram 
of the temperature ranges among optimal and absolute values, and a scatterplot of minimum temperature versus maximum altitude. 
These files are saved as 'rainfall_changes_prob.png', 'temp_diff.png', and 'Minimum_Temp_vs_Altitude.png', respectively in the 
'project_update_1' folder.







