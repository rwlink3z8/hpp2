raw_housing_table_string =("""
CREATE TABLE raw_house_mls_table (
    HOUSE_MLS_ID serial Primary Key,
    street_address text(250) NOT NULL,
    sale_price bigint NOT NULL,
    mls_number bigint NOT NULL,
    County TEXT,
    City TEXT,
    Subdivision TEXT,
    home_type TEXT,
    Floor_Plan TEXT,
    Bedrooms INT,
    Full_Baths INT,
    Half_Baths INT,
    Yr_Blt INT,
    Above_Grade_Finished_SF INT,
    Above_Grade_Finished_Source TEXT,
    Below_Grade_Finished_SF INT,
    Below_Grade_Finished_Source TEXT,
    Lot_Size TEXT,
    District TEXT,
    Fr_Pl TEXT,
    Fireplace TEXT,
    Bsmnt? TEXT,
    Bsmnt TEXT,
    Garage/Parking? TEXT,
    Construct TEXT,
    Arc_Style TEXT,
    Roof_desc TEXT,
    Lot_Desc TEXT,
    Floodpl TEXT,
    City_Limits TEXT,
    Cent air TEXT,
    Heating TEXT,
    Cooling TEXT,
    Water TEXT,
    Sewer TEXT,
    Warranty TEXT
);
""")

house_ll_string = ("""
CREATE TABLE HOUSE_LL (
	HOUSE_LL_ID serial PRIMARY KEY,
	HOUSE_LL_MAP_PIN VARCHAR ( 12 ) UNIQUE NOT NULL,
	HOUSE_LL_LATITUDE FLOAT ( 8 ) NOT NULL,
    	HOUSE_LL_LONGITUDE FLOAT ( 8 ) NOT NULL,
    	HOUSE_LL_SALE_PRICE bigint NOT NULL,
    	HOUSE_LL_BEDROOMS int NOT NULL,
    	HOUSE_LL_BATHROOMS float ( 2 ) NOT NULL
);
""")


raw_housing_table_insert = ("""
    INSERT INTO raw_house_mls_table (street_address, sale_price, mls_number, County, City, Subdivision, home_type, Floor_Plan, Bedrooms, Full_Baths, Half_Baths, Yr_Blt, Above_Grade_Finished_SF, Above_Grade_Finished_Source, Below_Grade_Finished_SF, Below_Grade_Finished_Source, Lot_Size, District, Fr_Pl, Fireplace, Bsmnt?, Bsmnt, Garage/Parking?, Construct, Arc_Style, Roof_desc, Lot_Desc, Floodpl, City_Limits, Cent air, Heating, Cooling, Water, Sewer, Warranty)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
"""
)

house_ll_insert = ("""
    INSERT INTO house_ll (HOUSE_LL_MAP_PIN, HOUSE_LL_LATITUDE, HOUSE_LL_LONGITUDE, HOUSE_LL_SALE_PRICE, HOUSE_LL_BEDROOMS, HOUSE_LL_BATHROOMS)
    VALUES(%s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
"""
)

# query lists
create_table_queries = [raw_housing_table_string, house_ll_string]

drop_table_queries = [raw_housing_table_string, house_ll_string]
