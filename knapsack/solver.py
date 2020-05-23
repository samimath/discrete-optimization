#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from operator import attrgetter

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

def dynamic_search(input_data):

    
def baseline(input_data):
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
            #print(taken)
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
        print('naive method:')
        print(naive(input_data))
        print('greedy search by sorting value density:')
        print(baseline(input_data))
        #print(get_weight_density(input_data))
    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
