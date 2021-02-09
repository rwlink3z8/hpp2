# Home Price Predictor 2

#### second house finished January 2021, close in early March!


## Data Collection and initial storage

The data is collected with a selenium webscraper, formatted and stored in a postgreql database with the following two files:
`house_scraper.py` and `house_scraper_src.py` - These can be run from the command line

`getAddres.py` - this file gets the addresses from coordinates using pyautogui, something I realized was missing from one of my tables, necessary to link them

`clean_lat_long.py` - this file takes the unformatted txt file, formats it for data analysis and saves it as a new csv file it can be run from the command line
It will ask for 4 inputs
1. path to the file of interest
2. file name of interest
3. path where you want the new file to be written
4. file name of new file

`house_ll_migration.sql` migrates the lat long data into a postgresql database in an EC2, will update with address, once I've confirmed that's correct.
As it was only one table I used regex to quickly format it. 
- Todo: write a file to handle new data with more automation

## TODO
### Data processing
- Convert cleaning functions into a pipeline to clean up workflow
### Data Analysis
### Data Visualization
### User interface
- Updating client side scripts for better UI - for example replace JS with JQUERY
