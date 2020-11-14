import numpy as np
import matplotlib.pyplot as plt


def show_graph(percent=True, sort_by_change=False, international_only=False, airline_code=None, amount_shown=None, reverse=False):

    file_filters = ''
    if percent:
        file_filters += '_percent'
    else:
        file_filters += '_flat'
    if sort_by_change and not percent:
        file_filters += '_sort_by_change'
    if airline_code:
        file_filters += f'_{airline_code}'
    if international_only:
        file_filters += '_international_only'
    else:
        file_filters += '_domestic_only'

    flat_changes = open(f'../../output/changes/change{file_filters}.csv', 'r')
    data_flat = flat_changes.readlines()
    data_flat.pop(0)
    amount_routes = len(data_flat)

    if reverse:
        data_flat.reverse()

    if amount_shown:
        if amount_shown > amount_routes:
            amount_shown = amount_routes
    else:
        amount_shown = amount_routes

    total = 0
    bar1 = []
    bar2 = []
    x_labels = []

    for line in data_flat[:amount_shown]:
        if line:
            data = line.split(',')
            if percent:
                bar1.append(round(100 * float(data[1]), 2))
                total += round(100 * float(data[1]), 2)
            else:
                bar1.append(float(data[1]))
                bar2.append(float(data[2]))
                total += float(data[1]) - float(data[2])
            x_labels.append(data[0])

    average = total / amount_shown
    x = np.linspace(-1, 1, amount_shown)
    y = [average]*amount_shown
    # plt.plot(x, y)

    fig, ax = plt.subplots()
    index = np.arange(amount_shown)

    bar_width = 0.3
    opacity = 1
    plt.bar(index, bar1, bar_width, alpha=opacity, color='#F85E00', label='Summer')
    if not percent:
        plt.bar(index + bar_width, bar2, bar_width, alpha=opacity, color='#5F4BB6', label='Autumn')
        plt.ylabel('Amount baggage')
    else:
        plt.ylabel('Change in %')
    plt.xlabel('Route')
    plt.title(f'change{file_filters}.csv')
    plt.suptitle(f'Average difference: {average}')
    plt.xticks(index + bar_width, x_labels, rotation='vertical')
    plt.legend()
    plt.tight_layout()
    plt.show()

def show_scores(international_only=False, airline_code=None, amount_shown=None):

    file_filters = ''
    if airline_code:
        file_filters += f'_{airline_code}'
    if international_only:
        file_filters += '_international_only'
    else:
        file_filters += '_domestic_only'

    flat_changes = open(f'../../output/scores/scores{file_filters}.csv', 'r')
    data_flat = flat_changes.readlines()
    headers_meta = data_flat.pop(0)
    meta = headers_meta.split(',')[-1].split('=')[1].split(' ')
    amount_routes = len(data_flat)

    if amount_shown:
        if amount_shown > amount_routes:
            amount_shown = amount_routes
    else:
        amount_shown = amount_routes

    total = 0
    bar1 = []
    x_labels = []

    for line in data_flat[:amount_shown]:
        if line:
            data = line.split(',')
            bar1.append(float(data[5]))
            total += float(data[5])
            x_labels.append(data[0])

    average = total / amount_shown

    fig, ax = plt.subplots()
    index = np.arange(amount_shown)

    bar_width = 0.5
    opacity = 1
    plt.bar(index, bar1, bar_width, alpha=opacity, color='#776472', label='Compound score')
    plt.ylabel('Compound score')
    plt.xlabel('Route')
    plt.title(f'scores{file_filters}.csv')
    plt.suptitle(f'Weights: total_people={meta[0]}, percent={meta[1]}, flat={meta[2]},')
    plt.xticks(index, x_labels, rotation='vertical')
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':

    airline_code = 'DY'
    # show_graph(percent=True, sort_by_change=False, international_only=False, airline_code=None, amount_shown=50, reverse=False)
    show_scores(international_only=False, airline_code=None, amount_shown=50)
