from time import sleep

from data_manager import DataManager

from analysis_models.airport_model import AirportModel

from analysis_models.bag_model import BagModel

if __name__ == '__main__':

    data_folder = '../data/'
    airport_metadata_filename = 'DimFlyplassProccesed.csv'
    amount_files = 62
    data_file_1 = 0

    dm = DataManager(data_folder, amount_files, airport_metadata_filename)

    # Import single file
    dm.read_data_files(data_file_1)
    # print(dm.airport_metadata)

    # Import all files
    # dm.read_all_data_files()
    # print(dm.bag_messages)

    airport_model = AirportModel(dm)
    bag_model = BagModel(dm)

    print(bag_model.dm.airport_model.airports)
