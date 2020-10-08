import pandas as pd


class DataManager:

    def __init__(self, data_folder, amount_files):
        self.bag_messages = None
        self.data_folder = data_folder
        self.amount_files = amount_files

    def get_missing_bags(self):
        pass

    def read_all_data_files(self):

        self._read_file(self.create_data_file_name('0'))

        for x in range(1, self.amount_files, 1):
            self._read_file(self.create_data_file_name(str(x)))

    def read_data_files(self, file_number):
        self._read_file(self, self.create_data_file_name(file_number))

    def _read_file(self, filename: str) -> None:
        data_path = self.data_folder + filename
        try:
            print('Reading data from', filename)
            df = pd.read_csv(data_path, error_bad_lines=False, index_col=False, dtype='unicode')
            if self.bag_messages is not None:
                self.bag_messages += df
            else:
                self.bag_messages = df
        except:
            print('Failed to read datafile:', data_path)
            return None

    def create_data_file_name(self, number):
        filename = 'dbo_' + number.zfill(5) + '.V_NTNU_Export.csv'
        return filename
