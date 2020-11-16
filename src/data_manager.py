from typing import Union

import pandas as pd


class DataManager:

    def __init__(self, data_folder='../data/', output_folder='../output/', amount_files=62,
                 airport_metadata_filename='DimFlyplassProccesed.csv'):
        self.bag_messages = None
        self.data_folder = data_folder
        self.output_folder = output_folder
        self.amount_files = amount_files
        self.airport_metadata_filename = airport_metadata_filename
        self.airport_metadata = self._read_file(self.data_folder + airport_metadata_filename)

    def read_multiple_data_files(self, file_indexes=None):
        if file_indexes:
            self.bag_messages = self._read_file(self._create_data_file_path(str(file_indexes.pop(0))))
        else:
            self.bag_messages = self._read_file(self._create_data_file_path('0'))
            file_indexes = range(1, self.amount_files, 1)

        for x in file_indexes:
            self.bag_messages = self.bag_messages.append(self._read_file(self._create_data_file_path(str(x))),
                                                         ignore_index=True)

    def read_data_files(self, file_number=0):
        data = self._read_file(self._create_data_file_path(file_number))
        if not self.bag_messages:
            self.bag_messages = data
        else:
            self.bag_messages.append(data)
        return data

    def _read_file(self, file_path: str):

        data_path = file_path
        try:
            print('Reading data from', data_path)
            return pd.read_csv(data_path, error_bad_lines=False, index_col=False, dtype='unicode')
        except:
            print('Failed to read datafile:', data_path)

        return None

    def _create_data_file_name(self, number: Union[str, int]) -> str:
        filename = 'dbo_' + str(number).zfill(5) + '.V_NTNU_Export.csv'
        return filename

    def _create_data_file_path(self, number: Union[str, int]) -> str:
        filename = 'dbo_' + str(number).zfill(5) + '.V_NTNU_Export.csv'
        return self.data_folder + filename

    def get_unique_values(self, column_name: str):
        # variable to hold the count
        cnt = 0

        # list to hold visited values
        visited = []

        # loop for counting the unique
        for i in range(0, len(self.bag_messages[column_name])):

            if self.bag_messages[column_name][i] not in visited:
                visited.append(self.bag_messages[column_name][i])

                cnt += 1

        return cnt, visited
