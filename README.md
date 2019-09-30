# Flatiron Module 4 Project
In this project, I aim to use the EPA's Air Quality System data to perform some predictive time series analysis on the forecasts of a variety of different air pollutants defined by the EPA. These *parameters*, in the parlance of the EPA, have very granular measurements available through the database over a long period of time. The AQS API makes it easy to collect such data for a variety of locations over different stretches of time, segmented by state and parameter.

## The Data
In some sense, this is a continuation of the Module 3 project for the Data Science immersive program at the Flatiron School in Chicago. In this project, we will use our custom module from the Module 3 project, `pyaqs` to handle easy interaction and fetching of daily summary data from the API. In the Module 3 project, our attention was focused towards annual summary data, which does not provide nearly enough granularity for sufficient time series analysis. The fetching and storing of this daily summary data is a time consuming task that is handled in the interactive Jupyter notebook [data_fetching](data_fetching.ipynb). After execution of the code in this notebook, which makes use of `pyaqs`, the dataframes are stored in raw CSV format, so as to minimize API load and maximize time efficiency. This raw data is stored in the [`data`](./data/) folder, and is in general far too large to be stored easily on github.

Data cleaning is thus handled in a separate Jupyter notebook, [data_cleaning](data_cleaning.ipynb), in which the daily summary data in raw format is aggregated by day and filtered to produce an easily digestible format. These dataframes will be stored for easy access in the [`cleaned_data`](./cleaned_data/) folder, the contents of which will be stored on github.

## Tools Used
This project makes use of a variety of tools that are generally standard in the world of Python data science. Please make sure you have these packages installed (or use Anaconda):
- Pandas
- Numpy
- sklearn
- statsmodels

## Project Structure
The outline of the project hierarchy is here:
- [`data`](./data/): home of the raw data in CSV format
- [`cleaned_data`](./cleaned_data): home of the cleaned and aggregated data in CSV format
- [preliminary_exploration](preliminary_exploration.ipynb): An interactive Jupyter notebook that shows the beginning steps of the analysis and data exploration process.
- [data_fetching](data_fetching.ipynb): An interactive Jupyter notebook that fetches AQS data
- [data_cleaning](data_cleaning.ipynb): An interactive Jupyter notebook that cleans raw AQS data and stores it for easy access.
- [data_analysis](data_analysis.ipynb): An interactive notebook that handles analysis of the cleaned data. For time efficiency when viewing in the future, this notebook should be the starting point unless you wish to download lots of AQS data manually.
- [non_technical_notebook](conclusions_and_visualizations.ipynb): An interactive notebook targetted at a non-technical audience that details the findings of my analysis.
- [pyaqs.py](pyaqs.py): A custom Python module to handle wrapping of AQS API requests to Pandas dataframes.