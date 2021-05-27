import pandas as pd 
import sqlalchemy as db
import psycopg2 as pg2
from sqlalchemy import create_engine


import aws_config as cred
from data_pipeline_src import *

def read_data_from_db():
# connect to the database and read in the data from the first county
    conn = pg2.connect(user=cred.user, dbname=cred.database, host=cred.host, port=cred.port, password=cred.passw)
    data = pd.read_sql("""SELECT * FROM kchouses1 where kchouses1.county like(Cass)""", conn)
    conn.close()
    return data

def data_to_storage(data):
    engine = db.create_engine(user=cred.user, dbname=cred.database, host=cred.host, port=cred.port, password=cred.passw)
    conn = engine.connect()
    data.to_sql('kchouses2', conn, if_exists='append')
    conn.auttocommit = True
    conn.close()


def clean_and_pipe_data():
    data = read_data_from_db
    data1 = (data.pipe(get_columns_of_interest)
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
    data_to_storage(data1)

if __name__=="__main__":
    clean_and_pipe_data()
    print('Data formatted and sent to table for modeling')
