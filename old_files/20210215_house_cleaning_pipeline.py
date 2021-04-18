import pandas as pd 
import numpy as np 

from data_cleaning_src import clean_lot_size, price_to_log, convert_categorical_cols, send_to_csv

df = pd.read_csv('20210209mlstest.csv')

df = (df.pipe(clean_lot_size)
        .pipe(price_to_log)
        .pipe(convert_categorical_cols)
        .pipe(fix_lees_summit)
        .pipe(send_to_csv))
print("data cleaned and file written")
