#!/usr/bin/python
# -*- coding: utf-8 -*-

def solve_it():
    import numpy as np
    # return a positive integer, as a string
    return np.random.randint(-10,10,1)

if __name__ == '__main__':
    print('This script submits the integer: %s\n' % solve_it())

