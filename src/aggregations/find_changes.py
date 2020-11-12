def find_changes(international_only=False, airline_code=None, minimum_threshold=None, threshold_both_ways=False):

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
            routes[route_key] = {'before': int(amount), 'after': 0}

    for line in data_autumn:
        if line:
            route_key, amount = line.split(',')
            if routes.get(route_key):
                routes[route_key]['after'] = int(amount)
            else:
                routes[route_key] = {'before': 0, 'after': int(amount)}

    routes_before_only = {}
    routes_after_only = {}
    keys_to_delete = []

    for k, v in routes.items():
        if not v['after']:
            routes_before_only[k] = v['before']
            keys_to_delete.append(k)
        elif not v['before']:
            routes_after_only[k] = v['after']
            keys_to_delete.append(k)
        elif minimum_threshold:
            if threshold_both_ways:
                if v['after'] <= minimum_threshold or v['before'] <= minimum_threshold:
                    keys_to_delete.append(k)
            else:
                if v['after'] <= minimum_threshold and v['before'] <= minimum_threshold:
                    keys_to_delete.append(k)

    for k in keys_to_delete:
        del routes[k]

    routes_sorted = dict(sorted(routes.items(), key=lambda x: x[1]['before'] / x[1]['after'], reverse=True))

    with open(f'../../output/changes/change_percent{file_filters}.csv', 'w') as file:
        file.write('route,change\n')
        for k, v in routes_sorted.items():
            change = round(v['before'] / v['after'], 2)
            routes_sorted[k]['change'] = change
            file.write(f'{k},{change}\n')

    with open(f'../../output/changes/change_flat_sort_by_change{file_filters}.csv', 'w') as file:
        file.write('route,summer,autumn,change\n')
        for k, v in routes_sorted.items():
            change = v['before'] - v['after']
            routes_sorted[k]['change'] = change
            file.write(f'{k},{v["before"]},{v["after"]},{change}\n')

    routes_sorted = dict(sorted(routes.items(), key=lambda x: x[1]['before'] - x[1]['after'], reverse=True))

    with open(f'../../output/changes/change_flat{file_filters}.csv', 'w') as file:
        file.write('route,summer,autumn,change\n')
        for k, v in routes_sorted.items():
            change = v['before'] - v['after']
            routes_sorted[k]['change'] = change
            file.write(f'{k},{v["before"]},{v["after"]},{change}\n')

    # with open('../output/only_before.csv', 'w') as file:
    #     file.write('route,baggage_amount\n')
    #     for k, v in routes_before_only.items():
    #         file.write(f'{k},{v}\n')
    #
    # with open('../output/only_after.csv', 'w') as file:
    #     file.write('route,baggage_amount\n')
    #     for k, v in routes_after_only.items():
    #         file.write(f'{k},{v}\n')


if __name__ == '__main__':

    airline_code = 'DY'
    find_changes(minimum_threshold=100, international_only=False, airline_code=None)
    find_changes(minimum_threshold=100, international_only=False, airline_code=airline_code)
    find_changes(minimum_threshold=100, international_only=True, airline_code=None)
    find_changes(minimum_threshold=100, international_only=True, airline_code=airline_code)
