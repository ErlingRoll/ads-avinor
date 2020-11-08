from data_manager import DataManager
from analysis_models.airport_model import AirportModel
from analysis_models.bag_model import BagModel

if __name__ == '__main__':

    data_folder = '../data/'
    airport_metadata_filename = 'DimFlyplassProccesed.csv'
    amount_files = 62
    data_file_1 = 0

    dm = DataManager(data_folder, amount_files, airport_metadata_filename)

    # Import data
    dm.read_multiple_data_files([0])

    airport_model = AirportModel(dm)
    bag_model = BagModel(dm)

    bag_model.get_routes()
