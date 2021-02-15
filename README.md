# Home Price Predictor 2

#### second house finished January 2021, close in early March! visualizations to follow




## Table of Contents
1. Current and Future Architechture
2. Data collection and initial storage
3. TODO - Data transformation, modeling and storage
4. TODO - Client side work to present models in a readable, practical way


## Current and Future Architechture - migration to staging area database complete

![Screenshot20210211](https://github.com/rwlink3z8/hpp2/blob/main/img/Screenshot20210211_1.jpg)

## Data Collection and initial storage
First create the database in the docker container

`sudo docker run -p 5432:5432 -d 
-e POSTGRES_PASSWORD=password 
-e POSTGRES_USER=username 
-e POSTGRES_DB=ccmo_housing_information 
-v pgdata:/var/lib/postgresql/dasudota 
postgres`

After  creating the postgresql server the raw data can be scraped and stored into a psql database with the following two files by running `house_scraper.py` from the command line assuming the `house_scraper_src.py` is in the same directory - this can be easily modified where it takes no url input.

`getAddres.py` - this file gets the addresses from coordinates using pyautogui, something I realized was missing from one of my tables, necessary to link them
##todo
This is going to be easily reverse engineered, since i have the addresses, I can make a few small changes to that workflow to get lat and long coordinates that are useful later on for folium visualizations.

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

`20210215_house_cleaning_pipeline.py` and `data_cleaning_src.py` clean the data to prepare it for modelling and can be run from the command line by running the 20210215_house_cleaning_pipeline.py file

- have fun with data analysis, modeling, and visualization

### Client side work to present models in a readable, practical way
- look at django vs flask for better sql integration
- Updating client side scripts for better UI - for example replace JS with JQUERY
- look at agent descriptions for buzzwords for NLP for future work
