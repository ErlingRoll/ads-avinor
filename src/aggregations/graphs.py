import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    amount_shown = 50

    routes = {}

    flat_changes = open('../output/change_flat.csv', 'r')
    data_flat = flat_changes.readlines()
    data_flat.pop(0)

    during_summer = []
    after_summer = []
    x_labels = []

    for line in data_flat[:amount_shown]:
        if line:
            data = line.split(',')
            during_summer.append(int(data[1]))
            after_summer.append(int(data[2]))
            x_labels.append(data[0])

    fig, ax = plt.subplots()
    index = np.arange(amount_shown)
    bar_width = 0.2
    opacity = 0.8

    rects1 = plt.bar(index, during_summer, bar_width,
                     alpha=opacity,
                     color='red',
                     label='During summer')

    rects2 = plt.bar(index + bar_width, after_summer, bar_width,
                     alpha=opacity,
                     color='pink',
                     label='After summer')

    plt.xlabel('Route')
    plt.ylabel('Amount baggage')
    plt.title('')
    plt.xticks(index + bar_width, x_labels, rotation='vertical')
    plt.legend()

    plt.tight_layout()
    plt.show()
