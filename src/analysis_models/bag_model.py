from src.data_manager import DataManager
import pandas


class BagModel:

    def __init__(self, dm: DataManager):
        self.dm = dm

    def get_missing_bags(self):
        self.dm.read_data_files()
        df = self.dm.bag_messages
        print(df)
        pass


hello = BagModel(DataManager())
hello.get_missing_bags()