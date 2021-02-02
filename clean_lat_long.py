import pandas as pd
import numpy as np

'''
this file takes the raw txt file and cleans it, formats the data for later data analysis and wraps it in a pipeline for ease of use
file path and file name variables will need to be changed to fit your file structure

I personally don't like the format for adding inputs as seen on lines 11-14 and 39-42 - but it does give print statements to help catch errors

'''

def read_in_data(data):
    ''' change file path and file name to match your directory and file naming convention examples below
        this function reads in the data and names the columns
    '''
    print("1.Input the path to the file c/users/path/to/file/")
    file_path = input()
    print("2.Input the name of the original file")
    file_name = input()
    data = pd.read_csv(file_path+file_name, header=None, index_col=False, names=['Name', 'Lat', 'Long', 'Info'])
    data.reset_index(drop=True, inplace=True)
    return data

def get_features(data):
    ''' takes in the dataframe after read_in_data function is run 
    and splits out the info column into its individual features '''
    data['price'] = data['Info'].apply(lambda x: x.split(' ')[0][2:])

    data['bedrooms'] = data['Info'].apply(lambda x: x.split( ' ')[1][0])

    data['bathrooms'] = data['Info'].apply(lambda x: x.split(' ')[2].split('ba')[0])
    return data
    
def reorder_cols(data):
    # get only the columns you need, don't want to keep the intermediate column
    cols = ['Name', 'Lat', 'Long', 'price', 'bedrooms', 'bathrooms']
    data = data[cols]
    return data
    
def format_idx_drop_duplicates (data):
    # rename variables and remove inplace to silence warnings
    data = data.drop_duplicates(subset=['Name'])
    data = data.reset_index(drop=True)
    return data

def write_file(data):
    # save as a new cleaned csv to the desired file path and file name
    print("3. Input the path to write the cleaned file c/users/path/to/file/")
    file_path_out = input()
    print("4. Input the csv file name")
    file_name_out = input() 
    return data.to_csv(file_path_out + file_name_out, index=False)
      
      
data = (data.pipe(read_in_data)
        .pipe(get_features)
        .pipe(reorder_cols)
        .pipe(format_idx_drop_duplicates)
        .pipe(write_file))
