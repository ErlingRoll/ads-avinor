
if __name__ == '__main__':

    flat_changes = open('../output/change_flat.csv', 'r')
    changes = flat_changes.readlines()
    changes.pop(0)

    sum_before = 0
    sum_after = 0
    for line in changes:
        if line:
            sum_before += int(line.split(',')[1])
            sum_after += int(line.split(',')[2])

    print('Sum during summer:', sum_before)
    print('Sum after summer:', sum_after)
