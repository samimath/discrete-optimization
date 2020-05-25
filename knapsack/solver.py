#!/usr/bin/python
# -*- coding: utf-8 -*-


import collections
from collections import namedtuple
from operator import attrgetter
import numpy as np
from datetime import datetime
Item = namedtuple("Item", ['index', 'value', 'weight'])

Item2 = namedtuple("Item2", ['index', 'value', 'weight', 'value_density'])


# establish baseline algorithm:

def get_weight_density(input_data):
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item2(i - 1, int(parts[0]), int(parts[1]), float(parts[0]) / float(parts[1])))
    # returns list of attributes ordered by value density in descending order
    return capacity, sorted(items, key=attrgetter('value_density'), reverse=True)


def memoization_1d(items, cap):
    K = cap
    D = np.empty([K + 1, len(items) + 1])
    D[:] = np.NaN
    w = 0
    v = 0

    for k in range(0, K + 1):

        # print('**',k,':')

        for j in range(0, len(items) + 1):  # in items:

            if np.isnan(D[k, j]):
                # if there is 0 capacity:
                if (j == 0):
                    D[:, 0] = 0

                elif (items[j - 1].weight <= k):
                    D[k, j] = max(items[j - 1].value + D[k - items[j - 1].weight, j - 1], D[k, j - 1])
                    # if D[k,j] > D[k,j-1]:# items[j-1].value + D[k-items[j-1].weight,j-1]:
                    # print(j)
                else:
                    D[k, j] = D[k, j - 1]
            else:
                pass

    return D


def find_next_row(r, c, items, D):
    R = D.shape[0]

    C = D.shape[0]
    if (c < 0) or (r <= 0):
        return

    if (r == 0):
        x = 0
        next_col = c
        next_row = r

    # check if it's lower right corner:
    if D[r, c] == D[r, c - 1]:

        x = 0
        next_col = c - 1
        next_row = r
    else:
        #print(c, ' is selected')
        x = 1
        next_col = c - 1
        next_row = r - items[c - 1].weight
        return c - 1, find_next_row(next_row, next_col, items, D)

    return find_next_row(next_row, next_col, items, D)


def flatten(iterable):
    results = []
    for i in iterable:
        if isinstance(i, collections.Iterable) and not isinstance(i, str):
            results.extend(flatten(i))
        else:
            results.append(i)
    return results


def solve_dp(input_data):
    cap, items = get_weight_density(input_data)
    D = memoization_1d(items, cap)
    #print(D)
    #print(D[-1, -1])
    opt_val = D[-1, -1]
    r = D.shape[0] - 1
    c = D.shape[1] - 1
    #print(r)
    #print(c)
    #print(items)
    selected = flatten(find_next_row(r, c, items, D))  # [0:c]

    return opt_val, [x for x in selected if x is not None]


def solve_it_greedy(input_data):
    # let's try to implement greedy algorithm first

    # get ordered list of items
    capacity, items = get_weight_density(input_data)

    # initialize variables:

    value = 0
    weight = 0
    value_density = 0
    taken = [0] * len(items)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


def solve_it_dp(input_data):
    # let's try to implement greedy algorithm first

    # get ordered list of items
    capacity, items = get_weight_density(input_data)
    #print(items)
    value, taken_items = solve_dp(input_data)
    # initialize variables:

    taken = [0] * len(items)

    for ind in taken_items:

        taken[items[ind].index] = 1

    output_data = str(int(value)) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

def solve_it(input_data):

    now = datetime.now()

    output_data = solve_it_dp(input_data)
    later = datetime.now()
    difference = (later - now).total_seconds()
    print('time taken:', difference)
    return output_data

def naive(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))

    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0] * len(items)

    for item in items:

        if weight + item.weight <= capacity:
            # take item with highest value density:
            taken[item.index] = 1
            # print(taken)
            value += item.value
            weight += item.weight

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        #print('naive method:')
        #print(naive(input_data))
        print('dynamic programming approach:')
        print(solve_it(input_data))
        # print(get_weight_density(input_data))
    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
