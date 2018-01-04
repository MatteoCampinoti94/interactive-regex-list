import curses
from .interactive_list import cutsmart, ceil, regex_comp

def read_op(fn, s, regex):
    so = s
    op = 0

    while True:
        c = fn()

def interactive_list(data):
    if type(data) != dict:
        raise TypeError('Function requires dictionary argument')
    for i in data:
        if type(data[i]) != str:
            raise TypeError('Function requires dictionary of string elements')

    max_line = 0
    for i in data:
        if len(data[i]) > max_line: max_line = len(data[i])

    results = [[i for i in data]]
