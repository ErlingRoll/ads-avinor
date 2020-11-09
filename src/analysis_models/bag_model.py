from datetime import datetime as dt
from data_manager import DataManager


class BagModel:

    def __init__(self, dm: DataManager):
        self.dm = dm

    def get_routes(self, start_date, end_date):

        start_date_parsed = dt.strptime(start_date, '%Y-%m-%d')
        end_date_parsed = dt.strptime(end_date, '%Y-%m-%d')

        # Get all airports in Norway
        norwegian_airports = self.dm.airport_model.get_airports()

        bag_messages = self.dm.bag_messages
        loading_interval = int(round(len(bag_messages) / 100))

        # unique_bag_numbers = {}
        unique_routes = {}

        for index, row in bag_messages.iterrows():

            # Get bag number
            bag_number = row['bagTagNumber']

            # For showing loading progress
            if index % loading_interval == 0:
                print('Getting routes:', (index * 100 / len(bag_messages) + 1), end='%\r')

            departure_airport = row['bagEventAirportIATA']
            destination_airport = row['bagFinalAirportIATA']
            timestamp = dt.strptime(row['sourceTimestamp'][:10], '%Y-%m-%d')
            airport_legs = row['LegArrayLength']
            action_code = row['bagEventCode']

            route_key = str(departure_airport) + '-' + str(destination_airport)

            # or not all(i in norwegian_airports for i in [departure_airport, destination_airport]) \
            # or destination_airport in norwegian_airports \
            # Ignore line if not valid
            try:
                if not (start_date_parsed < timestamp < end_date_parsed) \
                        or action_code != 'BagTagGenerated' \
                        or departure_airport == destination_airport \
                        or destination_airport in norwegian_airports:
                    continue
            except Exception as e:
                print(bag_number, e)

            # bag_row = unique_bag_numbers.get(bag_number)
            # if bag_row:
            #     unique_bag_numbers[bag_number].append(row)
            # else:
            #     unique_bag_numbers[bag_number] = [row]

            route_row = unique_routes.get(route_key)
            if route_row:
                unique_routes[route_key].append(row)
            else:
                unique_routes[route_key] = [row]

        # print('\nAmount of unique bag numbers:', len(unique_bag_numbers))
        print('Amount of unique routes:', len(unique_routes))

        unique_routes_sorted = dict(sorted(unique_routes.items(), key=lambda x: len(x[1]), reverse=True))

        with open(f'{self.dm.output_folder}routes_{start_date}_{end_date}_international_only.csv', 'w') as file:
            file.write('airport,baggage_amount\n')
            for k, v in unique_routes_sorted.items():
                file.write(k + ',' + str(len(v)) + '\n')

        print('Wrote results to file:', f'{self.dm.output_folder}routes_{start_date}_{end_date}')
