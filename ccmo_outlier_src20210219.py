import pandas as pd 
import numpy as np 

# convert the combination floor plans into principal floor plans - this lowers the model accuracy
# by .002% but simplifies it
split_styles = ['Other, Side/Side Split',
    'Side/Side Split, Split Entry',
    'Front/Back Split, Split Entry',
    'Atrium Split, Raised Ranch','Atrium Split',
    'Atrium Split, Front/Back Split',
    'Atrium Split, California Split',
    '2 Stories, Atrium Split',
    'Side/Side Split','Split Entry, Tri Level'
    'Atrium Split, Side/Side Split','Loft, Side/Side Split',
    'Side/Side Split, Tri Level', 'Other, Split Entry','Front/Back Split',
    'California Split','California Split, Front/Back Split', 'Tri Level',
    'Atrium Split, Side/Side Split', 'Split Entry, Tri Level']
one_half_stories = [ '1.5 Stories, Ranch',
    '1.5 Stories, 2 Stories',
    '1.5 Stories, Side/Side Split',
    '1.5 Stories, Earth Contact',
    'Raised 1.5 Story, Raised Ranch']
reverses = ['Ranch, Reverse 1.5 Story', '2 Stories, Reverse 1.5 Story']
others = ['Other', 'Other, Ranch']
ecothers = ['2 Stories, Earth Contact', 'Earth Contact, Ranch']
raised_fp = ['Raised Ranch, Split Entry','Raised Ranch, Ranch']

def pca_floor_plans(data):

    data['Floor_Plan'] = data['Floor_Plan'].replace(to_replace=split_styles, value='Split Entry')
    data['Floor_Plan'] = data['Floor_Plan'].replace(to_replace=one_half_stories, value='1.5 Stories')
    data['Floor_Plan'] = data['Floor_Plan'].replace(to_replace=raised_fp, value='Raised Ranch')
    data['Floor_Plan'] = data['Floor_Plan'].replace(to_replace='Bungalow, Ranch', 
                                                value='Bungalow')
    data['Floor_Plan'] = data['Floor_Plan'].replace(to_replace=reverses, 
                                                value='Reverse 1.5 Story')
    data['Floor_Plan'] = data['Floor_Plan'].replace(to_replace=others, 
                                                value='Ranch')
    data['Floor_Plan'] = data['Floor_Plan'].replace(to_replace=ecothers, 
                                                value='Earth Contact')
    return data

def outlier_removal(data):
    data = data[data['Lot_Size']<10.5]
    data = data[data['Above_Grade_Finished_SF']<6000]
    data = data[data['Above_Grade_Finished_SF']>500]
    data = data.loc[data['District'].apply(lambda x: x in ['Raymore-Peculiar',
                                                            'Belton','Pleasant Hill',
                                                            'Harrisonville','Sherwood',
                                                            'Lees Summit','Cass-Midway'])]
    return data

def create_dummy_columns(data1):
    data1 = pd.get_dummies(data=data1, columns=['City', 'District', 'Floor_Plan'], dtype='int64')
    return data1
