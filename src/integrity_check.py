from data_manager import DataManager
from analysis_models.airport_model import AirportModel
from analysis_models.bag_model import BagModel
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':

    data_folder = '../data/'
    output_folder = '../output/'
    airport_metadata_filename = 'DimFlyplassProccesed.csv'
    amount_files = 62
    data_file_1 = 0

    dm = DataManager(data_folder, output_folder, amount_files, airport_metadata_filename)

    # Import data
    dm.read_multiple_data_files()
    bags = dm.bag_messages
    bags['sourceTimestamp'] = pd.to_datetime(bags['sourceTimestamp'])
    bags.sort_values(by='sourceTimestamp')
    print(len(bags))
    filtered = bags[bags['bagEventCode'].map(lambda x: str(x) == 'BagTagGenerated')]
    print(len(filtered))
    bagsByDay = filtered['sourceTimestamp'].groupby(filtered['sourceTimestamp'].dt.floor('d')).size().reset_index(name='count')
    print(len(bagsByDay))
    print(bagsByDay)

    fig, ax1 = plt.subplots()
    x = bagsByDay['sourceTimestamp']
    y = bagsByDay['count']
    ax1.plot(x, y, 'g-')
    plt.ylabel('Bag tags generated')
    plt.xlabel('Date')
    plt.title('Bag tag generation frequency')
    plt.xticks(rotation=90)
    plt.legend()
    plt.show()
