from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions
from selenium.common import exceptions

from sqlalchemy import create_engine

import pandas as pd 
import numpy as np 

from house_scraper_src import scrape_MLS, split_newline_table, convert_to_arrays, get_addresses_from_list, convert_to_key_values, apply_kv_to_list, kv_list_to_df, zip_up_data, df_to_storage

print("enter the url to scrape")
url = input()

housing_table = scrape_MLS(url)

df1 = get_addresses_from_list(convert_to_arrays(split_newline_table(housing_table)))
df2 = kv_list_to_df(apply_kv_to_list(convert_to_arrays(split_newline_table(scrape_MLS(housing_table)))))

housing_data = zip_up_data(df1, df2)

df_to_storage(housing_data)
