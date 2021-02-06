# hpp2

## TODO
- migrating existing home price predictor data to a psql database for the two tables, with python as the server side language
- rebuilding scraper to run from the command line and then update the sql database - complete
- save raw text from scraper as well to be able to come back to this in the future
- Convert cleaning functions into a pipeline to clean up workflow
- reinstall idle to make getAddress.py more reproducible
- Updating client side scripts for better UI - for example replace JS with JQUERY


`getAddres.py` - this file gets the addresses from coordinates using pyautogui, something I realized was missing from one of my tables, necessary to link them

`house_ll_migration.sql` migrates the lat long data into a postgresql database in an EC2, will update with address, once I've confirmed that's correct.
As it was only one table I used regex to quickly format it. 
- Todo: write a file to handle new data with more automation

`clean_lat_long.py` - this file takes the unformatted txt file, formats it for data analysis and saves it as a new csv file it can be run from the command line
It will ask for 4 inputs
1. path to the file of interest
2. file name of interest
3. path where you want the new file to be written
4. file name of new file

`scraper_to_dataframe.py` runs from the command line, would need the MLS listings for this to work, could also adapt for any newline characater separated list, it will ask you to input the URL and then it will output the raw data into the postgresql database and onto a CSV.

`scraper_to_dataframe.py` was then replaced with two files 

`house_scraper.py` and `house_scraper_src.py` replaced scraper to dataframe for improved modularity.
