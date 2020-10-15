from typing import Tuple

from data_manager import DataManager


class AirportModel:

    def __init__(self, dm: DataManager):
        dm.airport_model = self
        self.dm = dm
        self.airports = self.get_airports()[1]

    def get_airports(self) -> Tuple[int, list]:
        # Get list of unique airport names
        column_name = 'AirportCode'

        # variable to hold the count
        cnt = 0

        # list to hold visited values
        visited = []

        # loop for counting the unique
        for i in range(0, len(self.dm.airport_metadata[column_name])):

            if self.dm.airport_metadata[column_name][i] not in visited:

                visited.append(self.dm.airport_metadata[column_name][i])

                cnt += 1

        return cnt, visited
