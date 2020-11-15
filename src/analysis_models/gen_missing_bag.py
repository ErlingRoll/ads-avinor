from src.data_manager import DataManager
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from itertools import chain
import matplotlib.dates as mdates
from matplotlib.pyplot import figure


def read_datafile(datetime, datatype, important_cols, file_path="../../data/dbo_00000.V_NTNU_Export.csv"):
    df = pd.read_csv(file_path, index_col=None, low_memory=False, header=0, dtype=datatype,
                     parse_dates=datetime, usecols=important_cols)
    #print(df.info(memory_usage='deep'))
    return df


def get_bag_dataframe(date_cols, datatype, important_cols, file_path="../../data/", number_of_files=61):
    print("Reading first entry")
    filename = file_path + 'dbo_' + str(0).zfill(5) + '.V_NTNU_Export.csv'
    df = read_datafile(date_cols, datatype, important_cols, filename)

    for i in range(number_of_files)[1:]:
        print("Reading file nr ", i)
        filename = file_path + 'dbo_' + str(i).zfill(5) + '.V_NTNU_Export.csv'
        df = df.append(read_datafile(date_cols, datatype, important_cols, filename), True).astype(datatype)
        #print(df.info(memory_usage='deep'))
    print("Done with reading to memory")
    return df


def get_missing_bagage(nr_of_files=1):
    df_dtype = {
        "bagTagNumber": "int64",
        "bagEventAirportIATA": "object",
        "bagFinalAirportIATA": "object"
    }
    df_timestamp = ["sourceTimestamp"]
    wanted_data = ["sourceTimestamp", "bagTagNumber", "bagEventAirportIATA", "bagFinalAirportIATA"]
    df = get_bag_dataframe(df_timestamp, df_dtype, wanted_data, number_of_files=nr_of_files)
    df = filter_international(df)
    df = filter_missing(df)
    with pd.option_context('display.max_rows', 100, 'display.max_columns', None):
        print(df.iloc[20000:20100])
    return df
    #df.to_csv("../../data/missing_bags.csv")


def filter_international(df: pd.DataFrame):
    norske_flyplass = pd.read_csv("../../data/DimFlyplassProccesed.csv", index_col=None, low_memory=False, header=0,
                                  usecols=["IATACode"])
    norske_flyplass = norske_flyplass.drop_duplicates().values.tolist()
    norske_flyplass = list(chain.from_iterable(norske_flyplass))
    df = df[df.bagEventAirportIATA.isin(norske_flyplass)]
    df = df[df.bagFinalAirportIATA.isin(norske_flyplass)]
    return df


def filter_missing(df: pd.DataFrame):
    ret = df.drop_duplicates(subset=["bagTagNumber"], keep=False)
    return ret


def plot_missing_baggage():
    df = get_missing_bagage(nr_of_files=1)
    start_date = df['sourceTimestamp'].iloc[0]
    end_date = df['sourceTimestamp'].iloc[-1]
    number = end_date - start_date
    lis = [None] * number.days
    dates = [None] * number.days
    current_day = start_date
    iterate = 0
    current_sum = 0
    for index, row in df.iterrows():
        if(row['sourceTimestamp']-current_day).days >= 1:
            lis[iterate] = current_sum
            dates[iterate] = current_day.date()
            current_day = row['sourceTimestamp']
            iterate = iterate + 1
            current_sum = 0
        else:
            current_sum = current_sum + 1
    print(lis)
    print(dates)
    figure(num=None, figsize=(10, 5), dpi=300, facecolor='w', edgecolor='b')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=4))
    plt.plot(dates, lis)
    plt.ylabel('Number of missing luggage')
    plt.xlabel('Dates')
    plt.gcf().autofmt_xdate()
    plt.show()


plot_missing_baggage()
