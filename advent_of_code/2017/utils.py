# !/bin/python3

import os
import sys
import inspect


def read_input(val_type=None, separator=None):
    if len(sys.argv) > 1:
        fname = sys.argv[1]
        if not os.path.exists(fname):
            if len(sys.argv) == 2:
                if val_type:
                    return val_type(sys.argv[1])
                return sys.argv[1]
            if val_type:
                return [val_type(value) for value in sys.argv[1:]]
            return sys.argv[1:]
    else:
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        fname = '{0}input.txt'.format(os.path.splitext(module.__file__)[0])

    if not os.path.exists(fname):
        return

    with open(fname) as f:
        inp = []
        for line in f.readlines():
            line = line.strip()
            if separator:
                values = line.split(separator)
            else:
                values = line

            if val_type:
                if type(values) is list:
                    values = [val_type(value) for value in values]
                else:
                    values = [val_type(values)]

            if len(values) == 1:
                values = values[0]

            inp.append(values)

        if len(inp) == 1:
            return inp[0]
        return inp
