def find_changes(international_only=False, airline_code=None, minimum_threshold=None, threshold_both_ways=False, people_weight=1.0, percent_weight=1.0, flat_weight=1.0):
    file_filters = ''
    if airline_code:
        file_filters += f'_{airline_code}'
    if international_only:
        file_filters += '_international_only'
    else:
        file_filters += '_domestic_only'

    file_summer = open(f'../../output/routes/routes_summer{file_filters}.csv', 'r')
    data_summer = file_summer.readlines()
    data_summer.pop(0)

    file_autumn = open(f'../../output/routes/routes_autumn{file_filters}.csv', 'r')
    data_autumn = file_autumn.readlines()
    data_autumn.pop(0)

    routes = {}

    for line in data_summer:
        if line:
            route_key, amount = line.split(',')
            routes[route_key] = {'summer': float(amount), 'autumn': 0.0}

    for line in data_autumn:
        if line:
            route_key, amount = line.split(',')
            if routes.get(route_key):
                routes[route_key]['autumn'] = float(amount)
            else:
                routes[route_key] = {'summer': 0.0, 'autumn': float(amount)}

    routes_summer_only = {}
    routes_autumn_only = {}
    keys_to_delete = []

    for k, v in routes.items():
        if not v['autumn']:
            routes_summer_only[k] = v['summer']
            keys_to_delete.append(k)
        elif not v['summer']:
            routes_autumn_only[k] = v['autumn']
            keys_to_delete.append(k)
        elif minimum_threshold:
            if threshold_both_ways:
                if v['autumn'] <= minimum_threshold or v['summer'] <= minimum_threshold:
                    keys_to_delete.append(k)
            else:
                if v['autumn'] <= minimum_threshold and v['summer'] <= minimum_threshold:
                    keys_to_delete.append(k)

    for k in keys_to_delete:
        del routes[k]

    # Estimate people
    for k, v in routes.items():
        routes[k]['people_summer'] = v['summer'] * 1.3
        routes[k]['people_autumn'] = v['autumn'] * 1.3

    routes_sorted = dict(sorted(routes.items(), key=lambda x: x[1]['people_summer'] / x[1]['people_autumn'], reverse=True))

    # Calculate percent change
    with open(f'../../output/changes/change_percent{file_filters}.csv', 'w') as file:
        file.write('route,change_percent\n')
        for k, v in routes_sorted.items():
            change_percent = v['people_summer'] / v['people_autumn']
            routes_sorted[k]['change_percent'] = change_percent
            file.write(f'{k},{change_percent}\n')

    # Calculate flat change
    with open(f'../../output/changes/change_flat_sort_by_change{file_filters}.csv', 'w') as file:
        file.write('route,people_summer,people_autumn,change_people_flat\n')
        for k, v in routes_sorted.items():
            change_people_flat = v['people_summer'] - v['people_autumn']
            routes_sorted[k]['change_people_flat'] = change_people_flat
            file.write(f'{k},{v["people_summer"]},{v["people_autumn"]},{change_people_flat}\n')

    # Sort by flat difference
    routes_sorted = dict(sorted(routes.items(), key=lambda x: x[1]['change_people_flat'], reverse=True))

    # Calculate flat change with sorted array
    with open(f'../../output/changes/change_flat{file_filters}.csv', 'w') as file:
        file.write('route,people_summer,people_autumn,change_people_flat\n')
        for k, v in routes_sorted.items():
            file.write(f'{k},{v["people_summer"]},{v["people_autumn"]},{v["change_people_flat"]}\n')

    routes_two_ways = {}
    for k, v in routes_sorted.items():
        alphabetical_key = '-'.join(sorted(k.split('-')))
        if not routes_two_ways.get(alphabetical_key):
            routes_two_ways[alphabetical_key] = {
                'people_summer': v['people_summer'],
                'people_autumn': v['people_autumn'],
                'change_percent': v['change_percent'],
                'change_people_flat': v['change_people_flat'],
                'amount_routes': 1
            }
        else:
            routes_two_ways[alphabetical_key] = {
                'people_summer':  int(round((routes_two_ways[alphabetical_key]['people_summer'] + v['people_summer']) / 2)),
                'people_autumn':  int(round((routes_two_ways[alphabetical_key]['people_autumn'] + v['people_autumn']) / 2)),
                'change_percent': round((routes_two_ways[alphabetical_key]['change_percent'] + v['change_percent']) / 2, 5),
                'change_people_flat': int(round((routes_two_ways[alphabetical_key]['change_people_flat'] + v['change_people_flat']) / 2)),
                'amount_routes': routes_two_ways[alphabetical_key]['amount_routes'] + 1
            }

    # Filter routes and find maximums and minimums
    people_summer = {'max': None, 'min': None}
    change_percent = {'max': None, 'min': None}
    change_people_flat = {'max': None, 'min': None}
    keys_to_delete = []
    for k, v in routes_two_ways.items():

        if v['amount_routes'] != 2:
            # print(f'Route {k} shows up {v["amount_routes"]} times')
            keys_to_delete.append(k)
            continue

        if not people_summer['max']:
            people_summer = {'max': v['people_summer'], 'min': v['people_summer']}
            change_percent = {'max': v['change_percent'], 'min': v['change_percent']}
            change_people_flat = {'max': v['change_people_flat'], 'min': v['change_people_flat']}

        if v['people_summer'] > people_summer['max']:
            people_summer['max'] = v['people_summer']
        elif v['people_summer'] < people_summer['min']:
            people_summer['min'] = v['people_summer']

        if v['change_percent'] > change_percent['max']:
            change_percent['max'] = v['change_percent']
        elif v['change_percent'] < change_percent['min']:
            change_percent['min'] = v['change_percent']

        if v['change_people_flat'] > change_people_flat['max']:
            change_people_flat['max'] = v['change_people_flat']
        elif v['change_people_flat'] < change_people_flat['min']:
            change_people_flat['min'] = v['change_people_flat']

    # Remove routes that only goes one way
    for k in keys_to_delete:
        del routes_two_ways[k]

    # Normalize attributes
    for k, v in routes_two_ways.items():
        routes_two_ways[k]['people_summer_norm'] = round(100 * (v['people_summer'] - people_summer['min']) / (people_summer['max'] - people_summer['min']), 2)
        routes_two_ways[k]['change_percent_norm'] = round(100 * (v['change_percent'] - change_percent['min']) / (change_percent['max'] - change_percent['min']), 2)
        routes_two_ways[k]['change_people_flat_norm'] = round(100 * (v['people_summer'] - change_people_flat['min']) / (change_people_flat['max'] - change_people_flat['min']), 2)

    # Calculate compound score
    max_score = None
    min_score = None
    for k, v in routes_two_ways.items():
        # print(f'{k}:', v['people_summer_norm'], v['change_percent_norm'], v['change_people_flat_norm'])
        score = round((v['people_summer_norm'] * people_weight) + (v['change_percent_norm'] * percent_weight) + (v['change_people_flat_norm'] * flat_weight),4)
        routes_two_ways[k]['score'] = score
        if not max_score or not min_score:
            max_score = score
            min_score = score
        if score > max_score:
            max_score = score
        elif score < min_score:
            min_score = score

    # Sort by score
    routes_sorted = dict(sorted(routes_two_ways.items(), key=lambda x: x[1]['score'], reverse=True))

    # Calculate normalized score
    with open(f'../../output/scores/scores{file_filters}.csv', 'w') as file:
        file.write(f'route,total_people_summer,change_percent,change_people_flat,score,score_normalized,meta={people_weight} {percent_weight} {flat_weight}\n')
        for k, v in routes_sorted.items():
            score_normalized = round(100 * (v['score'] - min_score) / (max_score - min_score), 2)
            file.write(f'{k},{v["people_summer"]},{v["change_percent"]},{v["change_people_flat"]},{v["score"]},{score_normalized}\n')

    # with open('../output/only_summer.csv', 'w') as file:
    #     file.write('route,baggage_amount\n')
    #     for k, v in routes_summer_only.items():
    #         file.write(f'{k},{v}\n')
    #
    # with open('../output/only_autumn.csv', 'w') as file:
    #     file.write('route,baggage_amount\n')
    #     for k, v in routes_autumn_only.items():
    #         file.write(f'{k},{v}\n')


if __name__ == '__main__':
    airline_code = 'DY'
    people_weight = 1
    percent_weight = 0.0001
    flat_weight = 0
    find_changes(minimum_threshold=100, international_only=False, airline_code=None, people_weight=people_weight, percent_weight=percent_weight, flat_weight=flat_weight)
    find_changes(minimum_threshold=100, international_only=False, airline_code=airline_code, people_weight=people_weight, percent_weight=percent_weight, flat_weight=flat_weight)
    find_changes(minimum_threshold=100, international_only=True, airline_code=None, people_weight=people_weight, percent_weight=percent_weight, flat_weight=flat_weight)
    find_changes(minimum_threshold=100, international_only=True, airline_code=airline_code, people_weight=people_weight, percent_weight=percent_weight, flat_weight=flat_weight)
