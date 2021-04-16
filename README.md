# Home Price Predictor 2

#### second house finished January 2021, close in early March! visualizations to follow



## Table of Contents
1. Current and Future Architechture
2. Data collection and initial storage
3. Data transformation, modeling and storage
4. TODO - Client side work to present models in a readable, practical way


## Current and Future Architechture - migration to staging area database complete

![Screenshot20210211](https://github.com/rwlink3z8/hpp2/blob/main/img/Screenshot20210211_1.jpg)

Making the switch from webscraping to API's has allowed me to obtain real estate listings for over 308,000 single-family homes sold in the KC metro area over the last 20 years for three different counties. This represents a 100 fold increase in the data and current work is to continue to scale this project.

The raw data for the smallest county is in the data folder in 3 chunks, that accounts for approximately 10% of the total data

All of the raw data is currently stored in a postgreSQL database, from there data is pulled in for cleaning and modeling with pandas.

## Data Collection and initial storage
The data was obtained with permission from the multiple listing system, from there it is stored in a postgresql database on an AWS RDS

The data is read in, cleaned

`getLatLong.py` - this file gets the lat and long coordinates from the address using geopy, geopandas and googles API which can be obtained from the GCP


After getting the address with the coordinates
`clean_lat_long.py` - this file takes the unformatted txt file, formats it for data analysis and saves it as a new csv file it can be run from the command line
It will ask for 4 inputs
1. path to the file of interest
2. file name of interest
3. path where you want the new file to be written
4. file name of new file
## todo 
 - finish migrating this to the psql server as well


`house_ll_migration.sql` migrates the lat long data into a postgresql database in a docker container, will update with address, once I've confirmed that's correct. - or reverse the order of that program, and then use `sql_queries.py` to populate the database.




### Data transformation, modeling and storage

`20210215_house_cleaning_pipeline.py` and `data_cleaning_src.py` clean the data to prepare it for modelling and can be run from the command line by running the 20210215_house_cleaning_pipeline.py file. At this point the data is ready for exploratory data analysis

After EDA and PCA `ccmo_outlier_removal.py` is run to prepare the dataset for modelling and prediction, it uses the functions written in `ccmo_outlier_src20200219.py`

- have fun with data analysis, modeling, and visualization

### Client side work to present models in a readable, practical way
- look at django vs flask for better sql integration
- Updating client side scripts for better UI - for example replace JS with JQUERY
- look at agent descriptions for buzzwords for NLP for future work
