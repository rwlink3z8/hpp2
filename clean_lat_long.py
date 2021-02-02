import pandas as pd
import numpy as np

'''
this file takes the raw txt file and cleans it, formats the data for later data analysis and wraps it in a pipeline for ease of use
file path and file name variables will need to be changed to fit your file structure
'''

def get_features(data):
    ''' takes in the dataframe after read_in_data function is run 
    and splits out the info column into its individual features '''
    data['price'] = data['Info'].apply(lambda x: x.split(' ')[0][2:])

    data['bedrooms'] = data['Info'].apply(lambda x: x.split( ' ')[1][0])

    data['bathrooms'] = data['Info'].apply(lambda x: x.split(' ')[2].split('ba')[0])
    return data
    
def reorder_cols(data):
    
    cols = ['Name', 'Lat', 'Long', 'price', 'bedrooms', 'bathrooms']
    data = data[cols]
    return data
    
def format_idx_drop_duplicates (data):
    # rename variables and remove inplace to silence warnings
    data = data.drop_duplicates(subset=['Name'])
    data = data.reset_index()
    return data
    
data = pd.read_csv(file_path+file_name, header=None, index_col=False, names=['Name', 'Lat', 'Long', 'Info'])
data = (data.pipe(get_features).pipe(reorder_cols).pipe(format_idx_drop_duplicates))
