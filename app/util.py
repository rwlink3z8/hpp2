import pickle
import json
# import numpy as np
import pandas as pd
from sklearn.preprocessing import PowerTransformer
from scipy.special import inv_boxcox

__model = None
__city = None
__data_columns = None


"""
def get_estimated_price(sqft, lot_size, bedrooms, bathrooms, yr_built, location):
    try:
        loc_index = __data_columns.index(location)
    except:
        loc_index = -1
    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = lot_size
    x[2] = bedrooms
    x[3] = bathrooms
    x[4] = yr_built
    if loc_index>=0:
        x[loc_index] = 1
    prediction = np.exp(__model.predict([x])[0])
    val = np.ndarray.item(prediction)
    value = '${:,.0f}'.format(val)
    return value
"""

dat_col = {"data_columns": ["city", "district", "total_sqft", "lot_size", "bedrooms", "bathrooms", "yr_built", "garage_size"]}

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    __data_columns = dat_col["data_columns"]

    global __model
    if __model is None:
        with open("/home/robert/cc2/app/data/stacked_pipe20210605.pickle", "rb") as f:
           __model = pickle.load(f)
  
    
    print("loading saved artifacts...done")


# not in use yet add postgres, docker, docker-compose first
def _get_lambda_from_power_transform(data):
    '''
    this helper function takes the yearly adjusted sale price and gets lambda for the price prediction
    todo ---- look at statsmodels for a cleaner method
    parameters
    ---------
    data - this is meant to be the y_adjusted_price from the dataframe
    returns
    ---------
    fitted lambda from either a yeo-johnson or box cox transformation
    '''
    pt = PowerTransformer(method='yeo-johnson')
    pt.fit(data[['y_adjusted_price']])
    return pt.lambdas_[0]


def predict_price(city, district, total_sqft, lot_size, bedrooms, bathrooms, yr_built, garage):
    """
    price prediction
    lambda was found to be 0.20522 - todo don't hard code this
    """
    lam = 0.205216
    x = [city, district, total_sqft, lot_size, bedrooms, bathrooms, yr_built, garage]
    cols = __data_columns
    data = pd.DataFrame(data=[x], columns=cols)
    prediction = inv_boxcox(__model.predict(data)[0], lam)
    return f"${round(prediction)}"


def get_location_names():
    
    global __city
    if __city is None:
        return [
            "Garden City",
            "Pleasant Hill",
            "Strasburg",
            "Archie",
            "Belton",
            "Harrisonville",
            "Raymore",
            "Drexel",
            "Cleveland",
            "Peculiar",
            "East Lynne",
            "Freeman",
            "Creighton",
            "Lake Winnebago",
            "Lees Summit",
            "Greenwood",
            "Loch Lloyd"]


def get_data_columns():
    return __data_columns


if __name__ == "__main__":
    load_saved_artifacts()
    print(predict_price("Belton", 3000, 5, 4, 3, 2021))
    print(predict_price("Raymore", 3000, 5, 4, 3, 2021))
