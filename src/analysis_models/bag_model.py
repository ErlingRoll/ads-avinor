from datetime import datetime as dt
from data_manager import DataManager


class BagModel:

    def __init__(self, dm: DataManager):
        self.dm = dm

    def get_routes(self, summer=True, international_only=False, airline_code=None):

        # Hard coded summer and autumn periods
        summer_period = {'start_date': '2020-07-1', 'end_date': '2020-08-15'}
        autumn_period = {'start_date': '2020-08-16', 'end_date': '2020-09-15'}

        # Set period for valid routes
        if summer:
            start_date = dt.strptime(summer_period['start_date'], '%Y-%m-%d')
            end_date = dt.strptime(summer_period['end_date'], '%Y-%m-%d')
        else:
            start_date = dt.strptime(autumn_period['start_date'], '%Y-%m-%d')
            end_date = dt.strptime(autumn_period['end_date'], '%Y-%m-%d')

        # Get all airports in Norway
        norwegian_airports = self.dm.airport_model.get_airports()

        # Get all bag messages loaded in memory
        bag_messages = self.dm.bag_messages

        # Specify progress printing threshold
        loading_interval = int(round(len(bag_messages) / 100))

        # Variables to hold accumulated data
        unique_bags = {}
        unique_routes = {}

        for index, row in bag_messages.iterrows():

            # Get bag number
            bag_number = row['bagTagNumber']

            # For showing loading progress
            if index % loading_interval == 0:
                print('Getting routes:', (index * 100 / len(bag_messages) + 1), end='%\r')

            airport_legs = int(row['LegArrayLength'])

            if airport_legs <= 0:
                continue

            departure_airport = row['bagEventAirportIATA']
            final_destination = row['bagFinalAirportIATA']
            timestamp = dt.strptime(row['sourceTimestamp'][:10], '%Y-%m-%d')
            second_last_airport = row[f'Leg{str(airport_legs - 1)}_departureAirportIATA']
            action_code = row['bagEventCode']

            try:
                if not (start_date < timestamp < end_date) \
                        or action_code != 'BagTagGenerated' \
                        or departure_airport == final_destination \
                        or departure_airport != second_last_airport:
                    continue

                is_domestic = all([i in norwegian_airports for i in [departure_airport, final_destination]])

                if is_domestic and international_only:
                    continue

                if not is_domestic and not international_only:
                    continue

            except Exception as e:
                print(bag_number, e)

            unique_bags[bag_number] = row

        # Process all legs of each baggage
        for bag_number, bag in unique_bags.items():
            for leg_number in range(int(bag['LegArrayLength'])):
                departure_airport = bag[f'Leg{str(leg_number)}_departureAirportIATA']
                arrival_airport = bag[f'Leg{str(leg_number)}_arrivalAirportIATA']
                _airline_code = bag[f'Leg{str(leg_number)}_operatingAirlineIATA']

                is_domestic = all([i in norwegian_airports for i in [departure_airport, arrival_airport]])

                if is_domestic and international_only:
                    continue

                if not is_domestic and not international_only:
                    continue

                # Skip if airline code does not match the one specified if it is specified
                if airline_code:
                    if airline_code != _airline_code:
                        continue

                route_key = str(departure_airport) + '-' + str(arrival_airport)
                route_row = unique_routes.get(route_key)
                if route_row:
                    unique_routes[route_key].append(bag)
                else:
                    unique_routes[route_key] = [bag]

        unique_routes_sorted = dict(sorted(unique_routes.items(), key=lambda x: len(x[1]), reverse=True))

        file_filters = ''
        if summer:
            file_filters += '_summer'
        else:
            file_filters += '_autumn'
        if airline_code:
            file_filters += f'_{airline_code}'
        if international_only:
            file_filters += '_international_only'
        else:
            file_filters += '_domestic_only'

        output_file = f'{self.dm.output_folder}routes{file_filters}.csv'

        total_bag_legs = 0

        with open(output_file, 'w') as file:
            file.write('airport,bag_amount\n')
            for k, v in unique_routes_sorted.items():
                file.write(k + ',' + str(len(v)) + '\n')
                total_bag_legs += len(v)

        print('\nAmount of unique bags:', len(unique_bags))
        print('Amount of unique routes:', len(unique_routes))
        print('Total bag legs flown:', total_bag_legs)
        print('Wrote results to file:', output_file)
