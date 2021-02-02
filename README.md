# hpp2

## TODO
- migrating existing home price predictor data to a psql database for the two tables, with python as the server side language, update JS to jquery for a more seamless UI
- rebuilding scraper to run from the command line and then update the sql database
- Convert cleaning functions into a pipeline to clean up workflow
- reinstall idle to make getAddress.py more reproducible
- Updating Site


`getAddres.py` - this file gets the addresses from coordinates using pyautogui, something I realized was missing from one of my tables, necessary to link them

`house_ll_migration.sql` migrates the lat long data into a postgresql database in an EC2, will update with address, once I've confirmed that's correct.
As it was only one table I was lazy and used regex to quickly format it. 
- Todo: write a file to handle new data with more automation

`clean_lat_long.py` 
