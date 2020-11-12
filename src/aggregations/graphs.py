import numpy as np
import matplotlib.pyplot as plt


def show_graph(percent=True, sort_by_change=False, international_only=False, airline_code=None, amount_shown=None):

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
            bar1.append(float(data[1]))
            if not percent:
                bar2.append(float(data[2]))
                total += float(data[1]) - float(data[2])
            else:
                total += float(data[1])
            x_labels.append(data[0])

    average = total / amount_shown
    x = np.linspace(-1, 1, amount_shown)
    y = [average]*amount_shown
    # plt.plot(x, y)

    fig, ax = plt.subplots()
    index = np.arange(amount_shown)

    bar_width = 0.3
    opacity = 0.9
    plt.bar(index, bar1, bar_width, alpha=opacity, color='#F85E00', label='Summer')
    if not percent:
        plt.bar(index + bar_width, bar2, bar_width, alpha=opacity, color='#5F4BB6', label='Autumn')
    plt.xlabel('Route')
    plt.ylabel('Amount baggage')
    plt.title(f'change{file_filters}.csv')
    plt.suptitle(f'Average difference: {average}')
    plt.xticks(index + bar_width, x_labels, rotation='vertical')
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':

    airline_code = 'DY'
    show_graph(percent=False, sort_by_change=False, international_only=False, airline_code=airline_code, amount_shown=None)
