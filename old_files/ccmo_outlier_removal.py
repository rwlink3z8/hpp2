import pandas as pd  
import numpy as np 
from ccmo_outlier_src20210219 import *

'''
This takes in the cleaned dataset, preps it for modelling and sends it to a csv, after pca and eda we are still left with 96% of the houses
'''


mod_data = pd.read_csv('20200217_mls_clean1.csv')

mod_data = (mod_data.pipe(pca_floor_plans)
                    .pipe(outlier_removal)
                    .pipe(create_dummy_columns))

mod_data.to_csv('20210219_ccmo_model_data.csv')
print("data is ready for production model")
