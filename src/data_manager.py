from typing import Union

import pandas as pd


class DataManager:

    def __init__(self, data_folder='../../data/', amount_files=62, airport_metadata_filename='DimFlyplassProccesed.csv'):
        self.bag_messages = None
        self.data_folder = data_folder
        self.amount_files = amount_files
        self.airport_metadata_filename = airport_metadata_filename

    def read_all_data_files(self):

        self._read_file(self._create_data_file_name('0'))

        for x in range(1, self.amount_files, 1):
            self._read_file(self._create_data_file_name(str(x)))

    def read_data_files(self, file_number=0):
        self._read_file(self._create_data_file_name(file_number))

    def _read_file(self, filename: str) -> None:
        data_path = self.data_folder + filename
        try:
            print('Reading data from', data_path)
            df = pd.read_csv(data_path, error_bad_lines=False, index_col=False, dtype='unicode')
            if self.bag_messages is not None:
                self.bag_messages += df
            else:
                self.bag_messages = df
        except:
            print('Failed to read datafile:', data_path)
            return None

    def _create_data_file_name(self, number: Union[str, int]) -> str:
        filename = 'dbo_' + str(number).zfill(5) + '.V_NTNU_Export.csv'
        return filename

    def get_unique_values(self, column_name: str):
        # variable to hold the count
        cnt = 0

        # list to hold visited values
        visited = []

        # loop for counting the unique
        # values in height
        for i in range(0, len(self.bag_messages[column_name])):

            if self.bag_messages[column_name][i] not in visited:

                visited.append(self.bag_messages[column_name][i])

                cnt += 1

        return cnt, visited
