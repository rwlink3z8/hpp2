import pandas as pd
import numpy as np
from datetime import datetime
from scipy.stats import boxcox, yeojohnson
from scipy.special import boxcox1p

def get_columns_of_interest(data):
    data_columns = ['City', 'Zip', 'Type', 'Sub', 'Bedrooms', 'Full Baths', 'Half Baths',
                'Lot Size', 'Total Finished SF', 'Above Grade Finished SF', 'Yr Blt', 
                'Fr Pl', 'Bsmnt?', 'Cent Air','Gar','Floor Plan', 'Style', 'Construct', 'Roof', 'Garage #', 
                'Fireplace #', 'District', 'Public Remarks', 'HOA Fees', 'HOA Fee Frequency', 
                'Sale Price', 'Close Dt', 'Patio', 'Pool']
    data = data[data_columns]
    data = data.reset_index(drop=True)
    return data

def drop_important_nulls(data):
    data = data.drop_duplicates()
    data = data.dropna(subset=['Total Finished SF'])
    data = data.reset_index(drop=True)
    return data

def fix_pool(data):
    data['Pool'] = data['Pool'].fillna('No Pool')
    return data

construction_set = (('Board/Batten','Wood Siding'),('Brick Trim, Frame','Brick & Frame'),('Frame, Lap','Frame'),
('Board/Batten, Brick Trim','Wood Siding Brick Trim'),('Stucco & Frame','Stucco'),('Frame, Stone Trim','frame'),
('Brick Trim, Wood Siding','Wood Siding'),('Board/Batten, Frame','Wood Siding'),('All Brick','Brick & Frame'),
('Stone Trim, Wood Siding','Wood Siding'),('Stucco','Stucco'),('Brick Trim, Lap','Lap'),('Stone Trim, Stucco','Stone Trim'),
('Stucco, Wood Siding','Stucco'),('Frame, Stucco','Stucco'),('Board/Batten, Stone Trim','Wood Siding Stone Trim'),
('Stone Trim, Stucco & Frame','Stucco & Stone Trim'),('Brick & Frame, Vinyl Siding','Brick Trim, Vinyl Siding'),
('Lap, Stone Trim','Lap'),('Lap, Wood Siding','Wood Siding'),('Brick Veneer, Vinyl Siding','Brick Trim, Vinyl Siding'),
('Frame, Metal Siding','Metal Siding'),('Board/Batten, Lap','Wood Siding'),('Stone Trim, Vinyl Siding','Vinyl Siding Stone Trim'),
('Frame, Stone Veneer','Frame'),('Concrete, Frame','Frame'),('Stone Veneer, Stucco','Stucco & Stone Trim'),('Brick & Frame, Wood Siding','Brick & Frame'),
('Brick Trim, Stucco','Brick Trim'),('Board/Batten, Stone Veneer','Wood Siding Stone Trim'),('Stone Veneer, Vinyl Siding','Vinyl Siding Stone Trim'),
('Brick Veneer, Frame','Wood Siding Stone Trim'),('Stone Veneer, Wood Siding','Wood Siding'),('Stucco & Frame, Wood Siding','Stucco'),
('Board/Batten, Brick & Frame','Wood Siding'),('Brick Trim, Metal Siding','Metal Siding'),('Board/Batten, Stucco','Wood Siding'),
('Brick & Frame, Frame','Brick & Frame'),('Lap, Stucco','Lap'),('Board/Batten, Wood Siding','Wood Siding'),
('Stone & Frame, Stucco','Stucco & Stone Trim'),('Stone & Frame, Wood Siding','Stone & Frame'),('Lap, Stone Veneer','Lap'),
('Board/Batten, Brick Veneer','Wood Siding Brick Trim'),('Brick Trim, Other','Brick Trim'),('Brick Veneer, Wood Siding','Brick Trim'),
('Frame, Other','Frame'),('Brick & Frame, Metal Siding','Brick & Frame'),('Stone & Frame, Stone Trim','Stone & Frame'),
('Board/Batten, Vinyl Siding','Wood Siding'),('Brick Trim, Stucco & Frame','Brick Trim'),('Brick & Frame, Brick Trim','Brick & Frame'),
('Stone & Frame, Stucco & Frame','Stone & Frame'),('Frame, Shingle/Shake','Frame'),('Cedar','Wood Siding'),
('Brick & Frame, Stucco','Brick & Frame'),('Brick Veneer','Brick Trim'),('Log','Wood Siding'),('Stucco & Frame, Vinyl Siding','Stucco'),
('Board/Batten, Stucco & Frame','Wood Siding'),('Lap, Vinyl Siding','Lap'),('Stone & Frame, Vinyl Siding','Stone & Frame'),
('Other, Vinyl Siding','Vinyl Siding'),('Stone Veneer, Stucco & Frame','Stone Trim'),('Cedar, Frame','Wood Siding'),
('Brick & Frame, Lap','Brick & Frame'),('Frame, Stone & Frame','Frame'),('All Brick, Vinyl Siding','Brick & Frame'),
('Frame, Stucco & Frame','Frame'),('Other, Stucco','Stucco'),('Lap, Other','Lap'),('Board/Batten, Stone & Frame','Wood Siding'),
('Vinyl Siding, Wood Siding','Vinyl Siding'),('All Brick, Frame','Brick & Frame'),('Stone Veneer','Stone Trim'),
('Concrete, Wood Siding','Wood Siding'),('Brick Trim, Cedar','Brick Trim'),('Board/Batten, Concrete','Wood Siding'),
('Lap, Stucco & Frame','Lap'),('Asbestos, Frame','Asbestos'),('Lap, Stone & Frame','Lap'),('Other, Stone Trim','Stone Trim'),
('Brick Trim, Stone Trim','Brick Trim'),('Stucco, Stucco & Frame','Stucco'),('Concrete, Vinyl Siding','Vinyl Siding'),
('Brick Veneer, Metal Siding','Brick Trim'),('Brick & Frame, Stone Trim','Brick & Frame'),('Shingle/Shake, Wood Siding','Other'),
('Brick & Frame, Stucco & Frame','Brick & Frame'),('Brick Trim, Concrete','Brick Trim'),('Cedar, Shingle/Shake','Wood Siding'),
('All Brick, Stucco','Brick & Frame'),('Brick & Frame, Shingle/Shake','Brick & Frame'),('Cedar, Vinyl Siding','Vinyl Siding'),
('Cedar, Wood Siding','Wood Siding'),('Metal Siding, Vinyl Siding','Metal Siding'),('Brick Veneer, Lap','Brick Trim'),
('All Stone','Stone & Frame'),('Metal Siding, Stone Veneer','Metal Siding'),('Synthetic Stucco','Stucco'),('Other, Wood Siding','Wood Siding'),
('Brick Trim, Shingle/Shake','Brick Trim'),('Board/Batten, Cedar','Wood Siding'),('Brick & Frame, Other','Brick & Frame'),
('Lap, Metal Siding','Lap'),('Metal Siding, Stone Trim','Metal Siding'),('Brick Veneer, Stucco','Brick Trim'),('All Brick, Lap','Brick & Frame'),
('Frame, Synthetic Stucco','Frame'),('All Brick, Concrete','Brick & Frame'),('Brick Veneer, Shingle/Shake','Brick Trim'),
('Board/Batten, Other','Wood Siding'),('All Brick, Stone Trim','Brick & Frame'),('All Brick, Other','Brick & Frame'),
('Brick & Frame, Cedar','Brick & Frame'),('Brick & Frame, Stone & Frame','Brick & Frame'),('All Brick, Board/Batten','Brick & Frame'),
('Brick Veneer, Other','Brick Trim'),('All Stone, Board/Batten','Stone & Frame'),('Frame, Log','Wood Siding'),('Asbestos, Lap','Asbestos'),
('Concrete, Lap','Concrete'),('Metal Siding, Other','Metal Siding'),('Brick Trim, Synthetic Stucco','Brick Trim'),('Brick Trim, Stone & Frame','Brick Trim'),
('Asbestos, Board/Batten','Asbestos'),('Board/Batten, Synthetic Stucco','Wood Siding'),('Board/Batten, Shingle/Shake','Wood Siding'),
('Cedar, Lap','Wood Siding'),('Board/Batten, Metal Siding','Wood Siding'),('Concrete, Stone & Frame','Stone & Frame'),('Log, Wood Siding','Wood Siding'),
('Synthetic Stucco, Wood Siding','Stucco'),('Metal Siding, Wood Siding','Metal Siding'),('All Brick, All Stone','Brick & Frame'),
('All Stone, Frame','Stone & Frame'),('Cedar, Stone & Frame','Stone & Frame'),('Concrete, Stucco','Stucco'),('Metal Siding, Stone & Frame','Metal Siding'),
('Concrete, Stone Veneer','Stone & Frame'),('All Brick, Metal Siding','Brick & Frame'),('All Brick, Wood Siding','Brick & Frame'),
('Shingle/Shake, Stone Trim','Other'),('All Brick, Brick Trim','Brick & Frame'),('Stone & Frame, Synthetic Stucco','Stone & Frame'),
('Block, Vinyl Siding','Vinyl Siding'),('Other, Stucco & Frame','Stucco'),('All Brick, Brick & Frame','Brick & Frame'),
('Stucco, Synthetic Stucco','Stucco'),('Cedar, Log','Wood Siding'),('Cedar, Metal Siding','Wood Siding'),('Board/Batten, Log','Wood Siding'),
('Cedar, Stone Trim','Wood Siding'),('Stone & Frame, Stone Veneer','Stone & Frame'),('Block, Wood Siding','Stone & Frame'),
('All Brick, Cedar','Brick & Frame'),('Brick & Frame, Concrete','Brick & Frame'),('Log, Other','Wood Siding'),('Asbestos, Shingle/Shake','Asbestos'),
('Other, Stone & Frame','Stone & Frame'),('Stone Trim, Stone Veneer','Stone Trim'),('Asbestos, Wood Siding','Asbestos'),
('Concrete, Stucco & Frame','Concrete'),('Brick Veneer, Stucco & Frame','Brick Trim'),('Lap, Shingle/Shake','Lap'),('Brick & Frame, Log','Brick & Frame'),
('Brick & Frame, Brick Veneer','Brick & Frame'),('Brick Trim, Log','Brick Trim'),('Other, Stone Veneer','Stone Trim'),('Concrete, Other','Concrete'),
('Shingle/Shake, Stone & Frame','Stone & Frame'),('Block, Frame','Stone & Frame'),('Brick Trim, Brick Veneer','Brick Trim'),('Block, Lap','Stone & Frame'),
('All Stone, Vinyl Siding','Stone & Frame'),('Brick Veneer, Log','Brick Trim'),('Other, Rolled','Other'),('All Brick, Shingle/Shake','Brick & Frame'),
('Brick Veneer, Concrete','Brick Trim'),('Brick & Frame, Synthetic Stucco','Brick & Frame'),('All Stone, Stucco','Stone & Frame'),
('Asbestos, Metal Siding','Asbestos'),('Block, Brick Veneer','Stone & Frame'),('Block, Stucco','Stone & Frame'),('Shingle/Shake, Vinyl Siding','Vinyl Siding'),
('Metal Siding, Synthetic Stucco','Metal Siding'),('All Brick, Block','Brick & Frame'),('All Brick, Stone Veneer','Brick & Frame'),
('Stucco & Frame, Synthetic Stucco','Stucco'),('All Brick, Stone & Frame','Brick & Frame'),('Frame, Radiant Barrier, Stone Trim','Frame'),
('All Stone, Other','Stone & Frame'),('Cedar, Stone Veneer','Wood Siding'),('All Stone, Brick & Frame','Brick & Frame'),
('Log, Vinyl Siding','Vinyl Siding'),('All Stone, Stone Trim','Stone & Frame'),('Metal Siding, Shingle/Shake','Metal Siding'),
('Concrete, Metal Siding','Concrete'),('Cedar, Other','Wood Siding'),('Brick Veneer, Cedar','Brick Trim'),('Brick Trim, Stone Veneer','Brick Trim'),
('Stone Veneer, Synthetic Stucco','Stucco'),('Lap, Synthetic Stucco','Lap'),('Brick Veneer, Stone Trim','Brick Trim'),
('Stone Trim, Synthetic Stucco','Stucco'),('Metal Siding, Stucco','Metal Siding'),('Brick & Frame, Stone Veneer','Brick & Frame'),
('Synthetic Stucco, Vinyl Siding','Vinyl Siding'),('Block, Concrete','Stone & Frame'),('Radiant Barrier, Stone Trim, Wood Siding','Wood Siding'),
('Lap, Log','Lap'),('Asbestos','Asbestos'),('Block', 'Stone & Frame'),('Brick & Frame','Brick & Frame'),('Brick Trim','Brick Trim'),
('Brick Trim, Vinyl Siding','Brick Trim, Vinyl Siding'),('Concrete','Concrete'),('Frame','Frame'),('Lap','Lap'),('Metal Siding','Metal Siding'),
('Shingle/Shake','Other'),('Stone & Frame','Stone & Frame'),('Stone Trim','Stone Trim'),('Stucco','Stucco'),('Stucco & Stone Trim','Stucco & Stone Trim'),
('Vinyl Siding','Vinyl Siding'),('Vinyl Siding Stone Trim','Vinyl Siding Stone Trim'),('Wood Siding','Wood Siding'),
('Wood Siding Brick Trim','Wood Siding Brick Trim'),('Wood Siding Stone Trim','Wood Siding Stone Trim'),('Other','Other'))


def construction_types(data):
    data['Construct'] = data['Construct'].map(dict(construction_set)).fillna('Other')
    return data

# fix floor plans
floor_plans=(('Other, Side/Side Split', 'Split Entry'), ('Side/Side Split, Split Entry', 'Split Entry'), 
('Front/Back Split, Split Entry', 'Split Entry'), ('Atrium Split, Raised Ranch', 'Split Entry'), ('Atrium Split', 'Split Entry'), 
('Atrium Split, Front/Back Split', 'Split Entry'), ('Atrium Split, California Split', 'Split Entry'), ('2 Stories, Atrium Split', 'Split Entry'), 
('Side/Side Split', 'Split Entry'), ('Split Entry, Tri Level', 'Split Entry'), ('Atrium Split, Side/Side Split', 'Split Entry'),
('Loft, Side/Side Split', 'Split Entry'), ('Side/Side Split, Tri Level', 'Split Entry'), ('Other, Split Entry', 'Split Entry'), 
('Front/Back Split', 'Split Entry'), ('California Split', 'Split Entry'), ('California Split, Front/Back Split', 'Split Entry'), 
('Tri Level', 'Split Entry'), ('1.5 Stories, Ranch', '1.5 Stories'), ('1.5 Stories, 2 Stories', '1.5 Stories'), 
('1.5 Stories, Side/Side Split', '1.5 Stories'), ('1.5 Stories, Earth Contact', '1.5 Stories'), ('Raised 1.5 Story, Raised Ranch', '1.5 Stories'),
('2 Stories, Earth Contact', '1.5 Stories'), ('Earth Contact, Ranch', '1.5 Stories'), ('Ranch, Reverse 1.5 Story', 'Reverse 1.5 Story'), 
('2 Stories, Reverse 1.5 Story', 'Reverse 1.5 Story'), ('Other', 'Ranch'), ('Other, Ranch', 'Ranch'), ('Raised Ranch, Split Entry', 'Raised Ranch'), 
('Raised Ranch, Ranch', 'Raised Ranch'), ('Bungalow, Ranch', 'Bungalow'), ('1.5 Stories, Bungalow', 'Bungalow'), 
('1.5 Stories, California Split', '1.5 Stories'), ('1.5 Stories, Front/Back Split', 'Split Entry'), ('1.5 Stories, Loft', '1.5 Stories'), 
('1.5 Stories, Other', '1.5 Stories'), ('1.5 Stories, Raised 1.5 Story', '1.5 Stories'), ('1.5 Stories, Raised Ranch', '1.5 Stories'), 
('1.5 Stories, Reverse 1.5 Story', 'Reverse 1.5 Story'), ('1.5 Stories, Split Entry', '1.5 Stories'), ('1.5 Stories, Tri Level', '1.5 Stories'), 
('2 Stories, 3 Stories', '3 Stories'), ('2 Stories, Bungalow', 'Bungalow'), ('2 Stories, California Split', '2 Stories'), 
('2 Stories, Front/Back Split', '2 Stories'), ('2 Stories, Other', '2 Stories'), ('2 Stories, Raised 1.5 Story', '2 Stories'), 
('2 Stories, Raised Ranch', 'Raised Ranch'), 
('2 Stories, Ranch', '2 Stories'), ('2 Stories, Side/Side Split', 'Split Entry'), ('2 Stories, Split Entry', 'Split Entry'), 
('2 Stories, Tri Level', '2 Stories'), ('Atrium Split, Other', 'Split Entry'), ('Atrium Split, Split Entry', 'Split Entry'), 
('Atrium Split, Tri Level', 'Split Entry'), ('Bungalow, Loft', 'Bungalow'), ('Bungalow, Raised Ranch', 'Bungalow'), 
('Bungalow, Side/Side Split', 'Bungalow'), ('California Split, Other', 'Split Entry'), ('California Split, Split Entry', 'Split Entry'), 
('Earth Contact, Front/Back Split', 'Split Entry'), ('Earth Contact, Other', 'Earth Contact'), ('Earth Contact, Reverse 1.5 Story', 'Earth Contact'), 
('Front/Back Split, Other', 'Split Entry'), ('Front/Back Split, Raised Ranch', 'Split Entry'), ('Front/Back Split, Reverse 1.5 Story', 'Split Entry'), 
('Front/Back Split, Side/Side Split', 'Split Entry'), ('Front/Back Split, Tri Level', 'Split Entry'), ('Loft, Ranch', 'Ranch'), 
('Other, Raised 1.5 Story', '1.5 Stories'), ('Other, Raised Ranch', 'Raised Ranch'), ('Other, Reverse 1.5 Story', 'Reverse 1.5 Story'), 
('Other, Tri Level', 'Split Entry'), ('Raised 1.5 Story', '1.5 Stories'), ('Raised 1.5 Story, Ranch', '1.5 Stories'), 
('Raised 1.5 Story, Reverse 1.5 Story', '1.5 Stories'), ('Raised 1.5 Story, Split Entry', 'Split Entry'), ('Raised 1.5 Story, Tri Level', '1.5 Stories'),
('Raised Ranch, Reverse 1.5 Story', 'Reverse 1.5 Story'), ('Raised Ranch, Side/Side Split', 'Raised Ranch'), 
('Ranch, Side/Side Split', 'Ranch'), ('Ranch, Split Entry', 'Split Entry'), ('Ranch, Tri Level', 'Ranch'), 
('Reverse 1.5 Story', 'Reverse 1.5 Story'), ('Reverse 1.5 Story, Split Entry', 'Reverse 1.5 Story'), ('1.5 Stories', '1.5 Stories'), 
('2 Stories', '2 Stories'), ('3 Stories', '3 Stories'), ('Bungalow', 'Bungalow'), ('Earth Contact', 'Earth Contact'), 
('Raised Ranch', 'Raised Ranch'), ('Ranch', 'Ranch'), ('Split Entry', 'Split Entry'))

def fix_floor_plans(data):
    data['Floor Plan'] = data['Floor Plan'].map(dict(floor_plans)).fillna('Other')
    return data

roof_types=(('Composition,Other','Composition'),('Composition,Metal','Metal'),('Other,Tile','Tile'),
('Composition,WoodShingle','WoodShingle'),('Metal,Other','Metal'),('Other,WoodShingle','Other'),
('Shake,WoodShingle','Shake'),('Composition,Concrete','Concrete'),('Metal,Tile','Metal'),
('Composition,Shake','Composition'),('Concrete,Tile','Tile'),('Composition,Metal','Metal'),('Composition,Other','Composition'),
('Metal,Other','Metal'),('Composition,WoodShingle''Other,Tile','Tile'),('Slate','Other'),('Shake,WoodShingle','WoodShingle'),
('Composition,Shake','Composition'),('Metal,Tile','Metal'),('Composition','Composition'),('Concrete','Concrete'),
('Metal','Metal'),('Other','Other'),('Tile','Tile'),('WoodShingle','WoodShingle'))

def fix_roof_types(data):
    data['Roof'] = data['Roof'].map(dict(roof_types)).fillna('Other')
    return data

def fix_hoa_fees(data):
    data['HOA Fees'] = data['HOA Fees'].fillna(value=0)
    data['HOA Fees'] = data['HOA Fees'].apply(lambda x: int(x))
    return data

def fix_hoa_frequency(data):
    hoa_dict = {'None':0, 'Annually':1, 'Monthly':12, 'Quarterly':4, 'Semi-Annually':2}
    data['HOA Fee Frequency'] = data['HOA Fee Frequency'].fillna(value=0)
    data['HOA Fee Frequency'] = data['HOA Fee Frequency'].replace(to_replace=hoa_dict.keys(), value=hoa_dict.values())
    return data

def hoa_cost(data):
    data['hoa_cost'] = data['HOA Fees'] * data['HOA Fee Frequency']
    return data

arc_styles=(('A-Frame,CapeCod','A-Frame'),('A-Frame,Contemporary','A-Frame'),('A-Frame,Other','A-Frame'),
('A-Frame,Traditional','A-Frame'),('AnteBellum','Victorian'),('AnteBellum,Traditional','Victorian'),
('CapeCod,Colonial','CapeCod'),('CapeCod,Traditional','CapeCod'),('CapeCod,Tudor','CapeCod'),
('Colonial,Contemporary','Colonial'),('Colonial,Traditional','Colonial'),('Colonial,Victorian','Victorian'),
('Contemporary','Contemporary'),('Contemporary,Other','Contemporary'),('Contemporary,Spanish','Spanish'),
('Contemporary,Traditional','Contemporary'),('Craftsman,Other','Craftsman'),('Craftsman,Victorian','Craftsman'),
('French,Traditional','French'),('Other,Spanish','Spanish'),('Other,Traditional','Traditional'),
('Other,Victorian','Victorian'),('Spanish,Traditional','Spanish'),('Traditional,Tudor','Tudor'),
('Traditional,Victorian','Victorian'),('A-Frame','A-Frame'),('CapeCod','CapeCod'),('Colonial','Colonial'),
('Contemporary','Contemporary'),('Craftsman','Craftsman'),('French','French'),('Spanish','Spanish'),
('Traditional','Traditional'),('Tudor','Tudor'),('Victorian','Victorian'),('Other','Other'))

def fix_arc_style(data):
    data['Style'] = data['Style'].map(dict(arc_styles)).fillna('Other')
    return data

def fix_lees_summit(data):
    # Lees Summit is entered 2 ways, correct this
    data['District'] = data['District'].replace(to_replace="Lee's Summit", 
                                                  value='Lees Summit')
    data['City'] = data['City'].replace(to_replace="Lee's Summit", 
                                                  value='Lees Summit')
    return data

def transform_city1(data, col='City'):
    city_list = ['Garden City', 'Pleasant Hill', 'Strasburg', 'Archie', 'Belton',
                    'Harrisonville', 'Raymore', 'Drexel', 'Cleveland', 'Peculiar',
                    'East Lynne', 'Freeman', 'Creighton', 'Lake Winnebago',
                    'Lees Summit', 'Other', 'Greenwood', 'Loch Lloyd']
    data = data[data[col].isin(city_list)]
    data = data.reset_index(drop=True)
    return data

city_set=(('GunnCity','EastLynne'),('Holden','EastLynne'),('Adrian','Archie'),
('Kingsville','Strasburg'),('Urich','Creighton'),('Raymore','Raymore'),('Belton','Belton'),
('PleasantHill','PleasantHill'),('Harrisonville','Harrisonville'),('Peculiar','Peculiar'),
('LeesSummit','LeesSummit'),('GardenCity','GardenCity'),('Archie','Archie'),('Cleveland','Cleveland'),
('LakeWinnebago','LakeWinnebago'),('Drexel','Drexel'),('LochLloyd','LochLloyd'),('Freeman','Freeman'),
('Creighton','Creighton'),('Greenwood','Greenwood'),('EastLynne','EastLynne'),
('Strasburg','Strasburg'),('Other','Raymore'))

def transform_city2(data, col='City'):
    '''
    there are some very small towns and I tried to lump them with the school district they belong to after 
    removing the citys that were incorrect
    '''
    data['city'] = data[col].map(dict(city_set)).dropna()
    data = data.reset_index(drop=True)
    return data

schools=(('Raymore-Peculiar','Raymore-Peculiar'),('Belton','Belton'),('PleasantHill','PleasantHill'),
('Harrisonville','Harrisonville'),('Sherwood','Sherwood'),('Cass-Midway','Cass-Midway'),('Archie','Archie'),
('LeesSummit','LeesSummit'),('Drexel','Drexel'),('EastLynne','EastLynne'),('Other','Other'),
('Strasburg','Strasburg'),('LoneJack','Strasburg'),('Freeman','Cass-Midway'),('Cleveland','Cass-Midway'),
('Holden','EastLynne'),('Kingsville','Strasburg'),('Adrian','Archie'),('GunnCity','EastLynne'))

def fix_district(data, col='District'):
    data[col] = data[col].map(dict(schools)).fillna('Other')
    return data

def fix_dates(data):
    '''
    this function converts Close Dt to a datetime object then splits year and month from it
    '''
    try:
        data['Close Dt'] = data['Close Dt'].apply(lambda x: datetime.strptime(x, "%m/%d/%Y"))
        data['year'] = pd.DatetimeIndex(data['Close Dt']).year 
        data['month'] = pd.DatetimeIndex(data['Close Dt']).month 
    except ValueError as err:
        data['Close Dt'] = data['Close Dt'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
        data['year'] = pd.DatetimeIndex(data['Close Dt']).year 
        data['month'] = pd.DatetimeIndex(data['Close Dt']).month 
    
    return data

def fix_year(data, col='Yr Blt'):
    yr_dict={0.0:2000,196.0:1996,1194.0:1994,78.0:1978,76.0:1976,
            16.0:2016,204.0:2004,51.0:1951,19.0:2019,1654.0:1954,
            1080.0:1980,94.0:1994,4.0:2004,1004.0:2004,97.0:1997,
            85.0:1985,50.0:1950,68.0:1968,1389.0:1989,99.0:1999}
    data[col] = data[col].replace(to_replace=yr_dict.keys(),value=yr_dict.values())
    data[col] = data[col].where(data[col] >=1800, 1995)
    return data


def transform_target_func(data, price_col='Sale Price'):
    '''
    this function normalizes price to the current years mean price to adjust for inflation
    y_adjusted price = ((sale price)*(current year mean price)) / (sale year mean price)
    find lambda for box cox transformation and then apply boxcox tranformation with lambda
    see docs for more information, see yeo-johnson for negative numbers
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.boxcox.html
    '''    
    years = sorted(data['year'].unique().tolist())
    means = [data.loc[data['year']==i].mean()[price_col] for i in years]
    # the following line is commented out to test with old data and the year mean is hard coded in
    #mean_ = data.loc[data['year']==current_year].mean()[price_col]
    mean_ = 281499
    price_index = [(j/mean_) for j in means]

    price_indices = dict(zip(years, price_index))
    data['price_index'] = data['year'].map(price_indices)
    data['y_adjusted_price'] = data[price_col]/data['price_index']
    # comment out next two lines and use sklearn PowerTransformer
    y, fit_lambda = boxcox(data['y_adjusted_price'], lmbda=None)
    data['sale_price'] = boxcox1p(data['y_adjusted_price'], fit_lambda)
    return data

def lot_transformation_function(data):
    # fix lot size - remove outliers greater than 40 acres, larger than 1500 convert to acres
    data['Lot Size'] = data['Lot Size'].fillna(.2)
    data = data.loc[~data['Lot Size'].between(40,1500, inclusive=False)]
    data.loc[data['Lot Size']<40, 'lot_size'] = data['Lot Size']
    data.loc[data['Lot Size']>1500, 'lot_size'] = data['Lot Size']/43560
    return data

def rename_columns(data):
    data = data.rename(columns={'Bedrooms':'bedrooms', 'Full Baths':'bathrooms',
                               'Half Baths':'half_bath', 'Total Finished SF':'total_sqft',
                               'Yr Blt':'yr_built', 'Fr Pl':'has_fireplace', 'Bsmnt?':'has_basement',
                               'Cent Air':'central_air','Gar':'has_garage',
                               'Floor Plan':'floor_plan', 'Style':'style','Garage #':'garage_size',
                               'Fireplace #':'num_of_fireplaces','District':'district','Pool':'pool',
                               'Construct':'construction','Roof':'roof'})
    return data
