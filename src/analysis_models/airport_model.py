from src.data_manager import DataManager


class AirportModel:

    def __init__(self, dm: DataManager):
        self.dm = dm

    def get_airports(self) -> list:
        # Get list of unique airport names
        pass