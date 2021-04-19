import numpy as np 
import pandas as pd 
import sqlalchemy as db
import psycopg2 as pg2

from config1 import *
from data_pipeline_src import *


conn = pg2.connect(user=username, dbname=database, host=awshost, port=port, password=passw)
df = pd.read_sql("""SELECT * FROM kchouses1 where kchouses1.county like(Cass)""", conn)
conn.close()

df1 = (df.pipe(get_columns_of_interest)
        .pipe(drop_important_nulls)
        .pipe(fix_floor_plans)
        .pipe(roof_types)
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
