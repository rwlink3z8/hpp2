import psycopg2 as pg2
from sql_queries20210210 import create_table_queries, drop_table_queries

def create_database():
    # connect to default database
    conn = pg2.connect(
        "host=localhost dbname=ccmo_housing_information user=username password=username")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS ccmo_housing_information")
    cur.execute(
        "CREATE DATABASE ccmo_housing_information WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # connect to housing database
    conn = pg2.connect(
        "host=localhost dbname=ccmo_housing_information user=username password=username")
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
