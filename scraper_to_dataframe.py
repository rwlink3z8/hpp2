from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions
from selenium.common import exceptions

import numpy as np
import pandas as pd

'''
this is a webscraper for scraping the entirety of each MLS listing with selenium, webdriver wait sped the scraper up significantly as opposed to just setting a sleep timer
one weird behavior I have noticed is that it sometimes clicks and adds duplicates, so I had it go an extra 10-15% of all entries to account for that
the scraper opens the MLS listing main page
then it clicks the first listing and grabs the wrapper table from each listing and clicks on the next listing
the data is then stored in a table of newline separated values
the four functions are then run in succession to convert the table into a dataframe
'''
url= "https://matrix.heartlandmls.com/Matrix/Public/Portal.aspx?L=1&k=990316X949Z&p=DE-77667588-490" 

feature_list = ['MLS Number','County', 'City', 'Sub Div', 'Type',
        'Floor Plan Description', 'Bdrms',
       'Baths Full', 'Baths Half','Year Built', 'Sqft Main', 
       'SQFT MAIN SOURCE', 'Below Grade Finished Sq Ft',
       'Below Grade Finished Sq Ft Source', 'Lot Size', 'School District',
       'Fireplace?', 'Fireplace Description',
       'Basement', 'Basement Description',
       'Garage/Parking?', 'Construction', 
       'Architecture', 'Roof',  'Lot Description',
      'In Floodplain', 'Inside City Limits', 
       'Street Maintenance','Central Air', 'Heat', 
       'Cool', 'Water','Sewer']

def scrape_MLS(url):
                                                                         
    raw_house_table = []
    ignored_exceptions = [exceptions.NoSuchElementException, exceptions.StaleElementReferenceException, exceptions.WebDriverException]
    driver = webdriver.Firefox()
    driver.get(url)
    driver.find_element_by_xpath("/html/body/form/div[3]/div/div/div[5]/div[3]/span[2]/div/div/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/span/a").click()
    time.sleep(5)
    # 500 total listings on this site but the scraper has some behavior i can't explain
    while True:
        if len(raw_house_table)>=570:
            print('done')
            break
        else:
            try:
                raw_house_table.append(driver.find_element_by_id("wrapperTable").text)
                WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[3]/div/div/div[5]/div[2]/div/div[1]/div/div/span/ul/li[2]/a"))).click()
            except (exceptions.NoSuchElementException, exceptions.StaleElementReferenceException) as err:
                time.sleep(15)
    return raw_house_table

def split_newline_table(rawdata):
    '''
    all the house information is in a table with new line characters separating all of the fields
    split the lines to make it more workable
    '''
    split_house_table = [rawdata[i].splitlines() for i in range(len(rawdata))]
    return split_house_table

def convert_to_arrays(lst):
    '''
    convert the table of strings into an array for dataframe construction
    '''
    np_arrays = [np.array(arr) for arr in lst]
    return np_arrays

def convert_to_key_values(arr, feature_list):
    '''
     I can see now that I did not use the list new as planned
     try and except is used because not all the listings will have all of the
     keys i need
    '''
    new = []

    for val in feature_list:
        try:
            # y finds the index of the next value which is what is wanted
            # z builds the array getting the value
            # z1 returns only that value, maybe a cleaner way to do this?
            y = (np.argwhere(arr==val)+1).flatten()
            z = np.where(arr==val, arr[y], None)
            z1 = z[z!=None][0]
            new.append(z1)
        except:
            new.append(None)
    return dict(zip(feature_list, new))

def apply_kv_to_list(lst1, arr_lst):
    new_list = []
    for i in range(len(arr_lst)):
        new_list.append(convert_to_key_values(arr_lst[i], feature_list))
    return new_list
