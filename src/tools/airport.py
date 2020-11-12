import pandas as pd
import numpy as np
import matplotlib as plt
import glob

path = "../../data/DimFlyplass.csv"
df = pd.read_csv(path, skiprows=1, index_col=None, header=None, low_memory=False)
df.columns = 'DimKey,DimAlternateKey,BatchId,DateFrom,DateTo,Description,IATACode,' \
             'LVOwned,WorldRegionCode,WorldRegionDescription,CountryCode,Country,' \
             'National,Schengen,Eu,Eøs,AirportCode,AirportCity,0,Null'.split(',')
print(df.shape)
df_norway = df_filtered = df[df['Country'] == "Norway"]
df_norway = df_norway[df_norway['AirportCode'] != "-1"]
df_norway = df_norway[df_norway['AirportCity'] != "Offshore"]
print(df_norway.shape)
df_norway = df_norway.reset_index(drop=True)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df_norway)

df_norway.to_csv("../data/DimFlyplassProccesed.csv")


