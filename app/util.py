import pickle
import json

# import numpy as np
import pandas as pd
from sklearn.preprocessing import PowerTransformer
from scipy.special import inv_boxcox

# to run locally uncomment out
# with open("/path/to/file/pickle_mod.pickle", "rb") as f:
# to run in docker use the following
with open("pickle_mod.pickle", "rb") as f:
    __model = pickle.load(f)



# not in use yet
def _get_lambda_from_power_transform(data):
    """
    this helper function takes the yearly adjusted sale price and gets lambda for the price prediction
    todo ---- look at statsmodels for a cleaner method
    parameters
    ---------
    data - this is meant to be the y_adjusted_price from the dataframe
    returns
    ---------
    fitted lambda from either a yeo-johnson or box cox transformation
    """
    pt = PowerTransformer(method="yeo-johnson")
    pt.fit(data[["y_adjusted_price"]])
    return pt.lambdas_[0]


def predict_price(
    city, district, total_sqft, lot_size, bedrooms, bathrooms, yr_built, garage
):
    """
    price prediction
    lambda was found to be 0.20522 - todo don't hard code this
    """
    lam = 0.205216
    x = [[city, district, total_sqft, lot_size, bedrooms, bathrooms, yr_built, garage]]
    cols = [
        "city",
        "district",
        "total_sqft",
        "lot_size",
        "bedrooms",
        "bathrooms",
        "yr_built",
        "garage",
    ]
    data = pd.DataFrame(data=x, columns=cols)
    prediction = inv_boxcox(__model.predict(data)[0], lam)
    return f"${round(prediction)}"


if __name__ == "__main__":
    print(predict_price("Belton", "Raymore-Peculiar", 3000, 5, 4, 3, 2021, 2))
    print(predict_price("Raymore", "Raymore-Peculiar", 3000, 5, 4, 3, 2021, 2))
