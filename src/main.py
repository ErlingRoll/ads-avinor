from data_manager import DataManager
from analysis_models.airport_model import AirportModel
from analysis_models.bag_model import BagModel

if __name__ == '__main__':

    data_folder = '../data/'
    output_folder = '../output/'
    airport_metadata_filename = 'DimFlyplassProccesed.csv'
    amount_files = 62
    data_file_1 = 0

    dm = DataManager(data_folder, output_folder, amount_files, airport_metadata_filename)

    # Import data
    dm.read_multiple_data_files([49, 50, 51, 52, 53, 54, 55, 56, 57])  # Uncomment for running summer analysis
    # dm.read_multiple_data_files([57, 58, 59, 60])  # Uncomment for running autumn analysis

    airport_model = AirportModel(dm)
    bag_model = BagModel(dm)

    # Run model
    airline_code = 'DY'  # Norwegian

    # Summer
    bag_model.get_routes(summer=True, international_only=False, airline_code=airline_code)
    # bag_model.get_routes(summer=True, international_only=False, airline_code=None)
    bag_model.get_routes(summer=True, international_only=True, airline_code=airline_code)
    # bag_model.get_routes(summer=True, international_only=True, airline_code=None)

    # Autumn
    # bag_model.get_routes(summer=False, international_only=False, airline_code=airline_code)
    # bag_model.get_routes(summer=False, international_only=False, airline_code=None)
    # bag_model.get_routes(summer=False, international_only=True, airline_code=airline_code)
    # bag_model.get_routes(summer=False, international_only=True, airline_code=None)
