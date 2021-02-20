import pandas as pd 
import numpy as np 
from geopy.geocoders import GoogleV3

'''
get lats and longs from addresses for making heat maps

requires geopandas, geopy, and googlemaps API

'''
API_KEY = 'your_api_key'

# get just the addresses, mls number and sales price from the data of interest
data = pd.read_csv('20210219_ccmo_model_data1.csv')
addresses = data[['street_address', 'sale_price', 'mls_number']]

# create a google location object
locator = GoogleV3(API_KEY)

# list comprehension for all the addresses in the dataframe 
# other map types work better with pandas, google maps has better data though
locs = [locator.geocode(addr) for addr in addresses.street_address]

# locs is a list of location objects, grab the latitude attribute and longitude attribute
latitudes = [loc.latitude for loc in locs]
longitudes = [loc.longitude for loc in locs]

addresses['latitude'] = latitudes
addresses['longitude'] = longitudes
