from data_manager import DataManager
import pandas


class BagModel:

    def __init__(self, dm: DataManager):
        self.dm = dm

    def get_routes(self):

        # Get all airports in Norway
        norwegian_airports = self.dm.airport_model.get_airports()

        bag_messages = self.dm.bag_messages
        loading_interval = int(round(len(bag_messages) / 100))

        unique_bag_numbers = {}
        unique_routes = {}

        for index, row in bag_messages.iterrows():

            # Get bag number
            bag_number = row['bagTagNumber']

            # For showing loading progress
            if index % loading_interval == 0:
                print((index * 100/len(bag_messages) + 1), end='%\r')

            departure_airport = row['bagEventAirportIATA']
            destination_airport = row['bagFinalAirportIATA']
            airport_legs = row['LegArrayLength']
            action_code = row['bagEventCode']

            route_key = str(departure_airport) + '-' + str(destination_airport)

            # Ignore line if not in norway
            try:
                if not all(i in norwegian_airports for i in [departure_airport, destination_airport])\
                        or int(airport_legs) != 1\
                        or departure_airport == destination_airport\
                        or action_code != 'BagTagGenerated':
                    continue
            except Exception as e:
                print(bag_number, e)

            bag_row = unique_bag_numbers.get(bag_number)
            if bag_row:
                unique_bag_numbers[bag_number].append(row)
            else:
                unique_bag_numbers[bag_number] = [row]

            route_row = unique_routes.get(route_key)
            if route_row:
                unique_routes[route_key].append(row)
            else:
                unique_routes[route_key] = [row]

        print('\nAmount of unique bag numbers:', len(unique_bag_numbers))
        print('Amount of unique routes:', len(unique_routes))

        unique_routes_sorted = dict(sorted(unique_routes.items(), key=lambda x: len(x[1])))

        for k, v in unique_routes_sorted.items():
            print(k, len(v))
