# hpp2

## TODO
- migrating existing home price predictor data to a sql database backend
- rebuilding scraper to run from the command line and then update the sql database
- Convert cleaning functions into a pipeline to clean up workflow
- Updating Site


`getAddres.py` - this file gets the addresses from coordinates using pyautogui, something I realized was missing from one of my tables, necessary to link them

`house_ll_migration.sql` migrates the lat long data into a postgresql database inside a docker container, will update with address, once I've confirmed that's correct
