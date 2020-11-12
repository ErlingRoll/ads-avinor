if __name__ == '__main__':

    routes = {}

    file_before = open('../output/routes_2020-07-1_2020-08-15.csv', 'r')
    data_before = file_before.readlines()

    file_after = open('../output/routes_2020-08-16_2020-09-15.csv', 'r')
    data_after = file_after.readlines()

    data_before.pop(0)
    data_after.pop(0)

    for line in data_before:
        if line:
            route_key, amount = line.split(',')
            routes[route_key] = {'before': int(amount), 'after': 0}

    for line in data_after:
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
        elif v['after'] <= 100 and v['before'] <= 100:
            keys_to_delete.append(k)

    for k in keys_to_delete:
        del routes[k]

    routes_sorted = dict(sorted(routes.items(), key=lambda x: x[1]['before'] / x[1]['after'], reverse=True))

    with open('../output/change_percent.csv', 'w') as file:
        file.write('route,change\n')
        for k, v in routes_sorted.items():
            change = round(v['before'] / v['after'], 2)
            routes_sorted[k]['change'] = change
            file.write(f'{k},{change}\n')
            # print(k, v)

    routes_sorted = dict(sorted(routes.items(), key=lambda x: x[1]['before'] - x[1]['after'], reverse=True))

    with open('../output/change_flat.csv', 'w') as file:
        file.write('route,during_summer,after_summer,change\n')
        for k, v in routes_sorted.items():
            change = v['before'] - v['after']
            routes_sorted[k]['change'] = change
            file.write(f'{k},{v["before"]},{v["after"]},{change}\n')
            # print(k, v)

    with open('../output/only_before.csv', 'w') as file:
        file.write('route,baggage_amount\n')
        for k, v in routes_before_only.items():
            file.write(f'{k},{v}\n')

    with open('../output/only_after.csv', 'w') as file:
        file.write('route,baggage_amount\n')
        for k, v in routes_after_only.items():
            file.write(f'{k},{v}\n')
