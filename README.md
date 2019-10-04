# Flatiron Module 4 Project
In this project, I aim to use the EPA's Air Quality System data to perform some predictive time series analysis on the forecasts of a variety of different air pollutants defined by the EPA. These *parameters*, in the parlance of the EPA, have very granular measurements available through the database over a long period of time. The AQS API makes it easy to collect such data for a variety of locations over different stretches of time, segmented by state and parameter, and moreover the AQS website has multiple pre-generated files for ease of use.

## The Data
In some sense, this is a continuation of the Module 3 project for the Data Science immersive program at the Flatiron School in Chicago. The raw data is downloaded directly from the EPA AQS website. This data is stored in a local [`raw_data`](./raw_data/) folder, and is in general far too large to be stored easily on github. Data cleaning is handled in a Jupyter notebook, [data_cleaning](data_cleaning.ipynb), in which the daily summary data in raw format is aggregated by day and filtered to produce an easily digestible format. These dataframes will be stored for easy access in the [`cleaned_data`](./cleaned_data/) folder, the contents of which will be stored on github. 

## Tools Used
This project makes use of a variety of tools that are generally standard in the world of Python data science. Please make sure you have these packages installed (or use Anaconda):
- Pandas
- Numpy
- sklearn
- statsmodels

## Project Structure
The outline of the project hierarchy is here:
- [`raw_data`](./raw_data/): home of the raw data in zipped CSV format. Not on github
- [`cleaned_data`](./cleaned_data/): home of the cleaned and aggregated data in CSV format
- [`results_data`](./results_data/): home of CSV files of computed results and metrics.
- [`intermediate_data`](./intermediate_data/): home of intermediate CSV files by parameter used in the cleaning process. Not on github.
- [`plots`](./plots/): home of generated plot files for all states and parameters. Lots of good imagery here!
- [preliminary_exploration](preliminary_exploration.ipynb): An interactive Jupyter notebook that shows the beginning steps of the analysis and data exploration process.
- [data_cleaning](data_cleaning.ipynb): An interactive Jupyter notebook that cleans raw AQS data and stores it for easy access.
- [preliminary_data_analysis](preliminary_data_analysis.ipynb): An introductory analysis notebook that does basic manipulations and exploration of what statistical tools may be helpful.
- [data_analysis](data_analysis.ipynb): An interactive notebook that handles full analysis and visualization of the cleaned data. For time efficiency when viewing in the future, this notebook should be the starting point unless you wish to go through the cleaning procedures themselves.
- [non_technical_notebook](conclusions_and_visualizations.ipynb): An interactive notebook targetted at a non-technical audience that details the findings of my analysis.
- [pyaqs.py](pyaqs.py): A custom Python module to handle wrapping of AQS API requests to Pandas dataframes.