from time import sleep

from data_manager import DataManager

if __name__ == '__main__':

    data_folder = '../data/'
    amount_files = 62
    data_file_1 = 1

    dm = DataManager(data_folder, amount_files)

    # Import single file
    # dm.read_data_files(data_file_1)
    # print(dm.bag_messages)

    # Import all files
    dm.read_all_data_files()
    print(dm.bag_messages)
