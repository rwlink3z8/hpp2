# Home Price Predictor 2

#### second house finished January 2021, close in early March! visualizations to follow



## Table of Contents
1. Current and Future Architechture
2. Data collection and initial storage
3. Data transformation, modeling and storage
4. TODO - Client side work to present models in a readable, practical way


## Current and Future Architechture - migration to staging area database complete

![Screenshot20210211](https://github.com/rwlink3z8/hpp2/blob/main/img/Screenshot20210211_1.jpg)


## Data Collection and initial storage
Making the switch from webscraping to API's has allowed me to obtain real estate listings for over 308,000 single-family homes sold in the KC metro area over the last 20 years for three different counties. This represents a 100 fold increase in the data and current work is to continue to scale this project.

The raw data for the smallest county is in the data folder in 3 chunks, that accounts for approximately 10% of the total data

All of the raw data is currently stored in a postgreSQL database, an example of pulling the data from the server and the transformation pipeline are in
`pipeline_model20210416.py` this uses the functions from `data_pipeline_src.py` It also shows the stacked regressor that had an accuracy of 85.8%, however this is not a marked improvement over a gradient boosting regressor with an accuracy score of 85.7%.. still need to look at the predict price for both to determine which to use for production.

`getLatLong.py` - this file gets the lat and long coordinates from the address using geopy, geopandas and googles API which can be obtained from the GCP

### House prices over time

![prices_over_time](https://github.com/rwlink3z8/hpp2/blob/main/img/Screenshot%202021-04-16%20152909.jpg)

Because of the long period of time (20 years) house prices had to be normalized, the code for this is in the function `transform_target_func` in the `data_pipeline_src.py` file, the mean for 2021 was divided by the yearly mean sales price and this index was then multiplied by the sales price to normalize prices. The Rothschild saying comes to mind looking at the price anomoly...in late 2001, can't help but think we'll see some mean reversion once the world gets back to normal.

### Normalized House Prices

![normalized_prices](https://github.com/rwlink3z8/hpp2/blob/main/img/Screenshot%202021-04-16%20155013.jpg)

the normalized house prices have a skew greater than 4, so a boxcox transformation was done to deal with skew, the following figure shows the sale price distribution before and after the transformation. YeoJohnson transformations were also done to deal with severely skewed features.

### House price distribution before and after transformation

![price_dist](https://github.com/rwlink3z8/hpp2/blob/main/img/Screenshot%202021-04-16%20154327.jpg)

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


### Client side work to present models in a readable, practical way
- look at django vs flask for better sql integration
- Updating client side scripts for better UI - for example replace JS with JQUERY
- look at agent descriptions for buzzwords for NLP for future work
