import os
import pandas as pd
from itertools import islice, cycle

def dataframe_creator(txtpath, dfname, dirpath):
    df = pd.read_csv(txtpath, header=None)
    ########## Pressure Data #######################
    Pressure_data = df.iloc[1::2,0]
    Pressure_data = pd.DataFrame(Pressure_data)

    Pressure_List = []
    for title,content in Pressure_data.iterrows():
        for a, b in content.items():
            pressure = b.split()
        
            Pressure_List.append(pressure)

    Pressure_series = pd.Series(Pressure_List, name='Pressure(Bar)')
    Pressure_series = Pressure_series.explode()
    ########## Parameter Data #####################
    parameters = df.iloc[0::2,:]                    
    parameters.iloc[0] = parameters.iloc[0].shift(-1)
    parameters = parameters.drop([0,9], axis=1)

    Parameter_headers = []
    Parameter_data = []
    for title, content in parameters.iterrows():
        data_grab = []
        headers_grab = []

        for a, b in content.items():
            names = b.split(':')[0]
            info = b.split(':')[-1]

            data_grab.append(info)

            headers_grab.append(names)
            
        Parameter_data.append(data_grab)
        Parameter_headers.append(headers_grab)
    
    Parameter_df = pd.DataFrame(Parameter_data, columns=Parameter_headers[0])
    ###### Combines Pressure and Parameter Data ################################
    Final_df = pd.concat([Pressure_series,Parameter_df],axis=1)

    Final_df.rename(columns={' Parameters': 'Phi'}, inplace=True) #Note that the txt parameter names have a single space that must be included when calling!
    Final_df.rename(columns={' Fuel Type': 'Fuel Type'}, inplace=True)
    Final_df.rename(columns={' Chamber Air Temp': 'Chamber Air Temp'}, inplace=True)
    Final_df.rename(columns={' Inj Press': 'Inj Press'}, inplace=True)
    Final_df.rename(columns={' DOI': 'DOI'}, inplace=True)
    Final_df.rename(columns={' Chamber Press': 'Chamber Press'}, inplace=True)
    Final_df.rename(columns={' Period': 'Period'}, inplace=True)
    Final_df.rename(columns={' Wall Temp': 'Wall Temp'}, inplace=True)

    Final_df = Final_df.astype({'Pressure(Bar)': float, 'Phi': str, 'Fuel Type': str, 'Chamber Air Temp': str, 'Inj Press': float, 'DOI': float, 'Chamber Press': float,
                            'Period': float, 'Wall Temp': float})
    
    # for some reason 'Chamber Air Temp' throws an error if it isn't a string...idk why.
    
    timellist = []
    for i in range(len(Final_df.loc[0, 'Period'])):
        timellist.append(i*1000)

    Final_df = Final_df.assign(new_column=[*islice(cycle(timellist), len(Final_df))])

    Final_df['Time'] = Final_df['Period'].mul(Final_df['new_column'])
    Final_df = Final_df.drop('new_column', axis=1)

    Final_df.index.name = 'Inj Num'

    Final_df.to_csv(dirpath + '\\' + dfname + '.csv')

def parser_df(filepath):
    for dirpath, dirs, files in os.walk(filepath):
        for filename in files:
            fname = os.path.splitext(filename)
            if filename.endswith('.txt'):
                
                pathway = (dirpath + '\\' + fname[0] + fname[1])
                title = fname[0]

                dataframe_creator(pathway, title, dirpath)

# file = "C:\\Users\\cadea\\OneDrive\\Desktop\\CID Data Processing\\10bar_isooctane_0p5_phi\\10bar_isooctane_0p5_phi"
# parser_df(file)