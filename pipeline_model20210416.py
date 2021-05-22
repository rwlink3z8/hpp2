import numpy as np 
import pandas as pd 
import sqlalchemy as db
import psycopg2 as pg2

from sklearn.linear_model import Lasso, RidgeCV
from sklearn.ensemble import GradientBoostingRegressor, StackingRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import RobustScaler, PowerTransformer, OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin, RegressorMixin, clone
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.metrics import mean_squared_error  

import aws_config as cred
from data_pipeline_src import *

# connect to the database and read in the data from the first county
conn = pg2.connect(user=cred.user, dbname=cred.database, host=cred.host, port=cred.port, password=cred.passw)
df = pd.read_sql("""SELECT * FROM kchouses1 where kchouses1.county like(Cass)""", conn)
conn.close()

df1 = (df.pipe(get_columns_of_interest)
        .pipe(drop_important_nulls)
        .pipe(fix_floor_plans)
        .pipe(fix_roof_types)
        .pipe(fix_hoa_fees)
        .pipe(fix_hoa_frequency)
        .pipe(hoa_cost)
        .pipe(fix_arc_style)
        .pipe(fix_lees_summit)
        .pipe(transform_city1)
        .pipe(transform_city2)
        .pipe(fix_dates)
        .pipe(fix_year)
        .pipe(transform_target_func)
        .pipe(lot_transformation_function)
        .pipe(fix_district)
        .pipe(construction_types))

X = df1[['City','Bedrooms', 'Full Baths', 'Half Baths','Total Finished SF','Yr Blt',
       'Fr Pl', 'Bsmnt?', 'Cent Air', 'Gar', 'Floor Plan', 'Style','Garage #', 'Fireplace #', 'District',
       'Pool', 'hoa_cost', 'lot_size1', 'Construct', 'Roof']]
y = df1['sale_price'] 

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

numeric_features = ['Bedrooms', 'Full Baths','Garage #', 'Fireplace #']
categorical_features = ['City', 'Style','Construct', 'Floor Plan','Fr Pl', 'Bsmnt?', 'Cent Air', 'Gar',
                         'Roof','District', 'Pool']
skewed_features = ['Total Finished SF', 'Half Baths', 'hoa_cost', 'lot_size1', 'Yr Blt']


pt = PowerTransformer(standardize=False)
scaler = RobustScaler(with_centering=False)
#transformer = FunctionTransformer(transformation_function) come back to this
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')

numeric_transformer = Pipeline(steps=[('s', scaler), ('i', imputer)])
#numeric_transformer = Pipeline(steps=[('s', scaler), ('t', transformer), ('i', imputer)])

skewed_transformer = Pipeline(steps=[('pt', pt), ('s', scaler), ('i', imputer)])

categorical_transformer = Pipeline(steps=[
    ('i', SimpleImputer(strategy='constant', fill_value='Other')),
    ('onehot', OneHotEncoder(handle_unknown='error', drop='first'))])

preprocessor = ColumnTransformer(
    transformers=[('skewed', skewed_transformer, skewed_features),
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])


gboost = GradientBoostingRegressor(n_estimators=3000, learning_rate=0.05,
                                   max_depth=4, max_features='sqrt',
                                   min_samples_leaf=15, min_samples_split=10, 
                                   loss='huber', random_state =5)

lasso = Lasso(alpha=0.0005, random_state=1)

estimators = [('GB', gboost), ('lasso', lasso)]
stacked_pipe = Pipeline(steps=[('preprocessor', preprocessor),
                                ('stacked', StackingRegressor(estimators=estimators,
                                final_estimator=RidgeCV()))])
