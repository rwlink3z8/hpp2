import pandas as pd 
import numpy as np 

import sqlalchemy as db
import psycopg2 as pg2

'''
This file pulls the data from the staging database in psql, and cleans the data for modeling
alternatively you can 

'''
def read_in_data(engine_string):
    engine = db.create_engine(engine_string)

    query1 = '''
        SELECT * FROM raw_housing_table;
        '''
    query_df = pd.read_sql(query1, engine)
    return query_df

# engine_string = "postgres+psycopg2://username:password@localhost:5432/db_name"
# df = read_in_data(engine_string)




def clean_lot_size(data):

    '''
        lot size is formatted in a few ways 
        either as dimensions feetXfeet 
        in acres denoted by num_acres ac
        or in square feet num
        this function takes in a dataframe and a column, creates a temp df and converts everything 
        to acres as a float
    '''
    # this makes a temp dataframe with 3 columns by extracting the values 
    data1 = (data['Lot_Size'].str.replace(',','')
            .str.extract('([\.\d]+)\s?(ac|X)?([\.\d,]+)?'))
    # cast these as floats
    data1[[0,2]] = data1[[0,2]].astype(float)
    # convert everything to acres
    data['Lot_Size'] = np.select((data1[1].eq('X'), data1[1].eq('ac')),
                          (data1[0]* data1[2]/43560,data1[0]), 
                          data1[0]/43560 )
    return data

def price_to_log(data):
    '''
    looking at the skew of sale price with 
    data['sale_price].skew() you find it's 3.62
    converting sale price to log 
    np.log(df['sale_price']).skew() reduces the skew to -0.22
    add a column for log of sale price  
    '''
    data['log_price'] = data['sale_price'].apply(lambda x: np.log(x))
    return data

def convert_categorical_cols(data):
    '''
    Fr_Pl, Bsmnt?, Garage/Parking?, Floodpl, City_Limits, Cent air all have categorical variables

    '''
    try:
        data['Fr_Pl'] = data['Fr_Pl'].replace({'No':0,'Yes':1, 'Unknown':0})
        data['Bsmnt?'] = data['Bsmnt?'].replace({'No':0,'Yes':1, 'Unknown':0})
        data['Garage/Parking?'] = data['Garage/Parking?'].replace({'No':0,'Yes':1, 'Unknown':0})
        data['Floodpl'] = data['Floodpl'].replace({'No':0,'Yes':1, 'Unknown':0})
        data['City_Limits'] = data['City_Limits'].replace({'No':0,'Yes':1, 'Unknown':0})
        data['Cent air'] = data['Cent air'].replace({'No':0,'Yes':1, 'Unknown':0})
    except TypeError as err:
        print("check your function for errors - column names probably")
    return data

def fix_lees_summit(data):
    # Lees Summit is entered 2 ways, correct this
    data['District'] = data['District'].replace(to_replace="Lee's Summit", 
                                                  value='Lees Summit')
    data['City'] = data['City'].replace(to_replace="Lee's Summit", 
                                                  value='Lees Summit')
    return data


def send_to_csv(data):
    data.to_csv('20200215_mls_clean.csv')
