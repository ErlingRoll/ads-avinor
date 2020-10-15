from data_manager import DataManager
import pandas


class BagModel:

    def __init__(self, dm: DataManager):
        self.dm = dm

    def get_missing_bags(self):

        airports = self.dm.airport_model
        print(airports)
