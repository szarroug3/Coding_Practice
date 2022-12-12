# !/bin/python3

import inspect
import os
import sys


def read_input(val_type=None, delimiter='\n', line_delimiter=None, ignore_empty=True, line_ignore_empty=True, fname=None):
    if not fname:
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
        for line in f.read().split(delimiter):
            if ignore_empty:
                line = line.strip()
            else:
                line = line.replace('\n', '').replace('\r', '')

            if ignore_empty and line == '':
                continue

            if line_delimiter:
                values = line.split(line_delimiter)
            elif line_delimiter == '':
                values = list(line)
            else:
                values = line

            if line_ignore_empty:
                if type(values) is list:
                    values = [value.strip() for value in values]
                else:
                    values = values.strip()

            if val_type:
                if type(values) is list and type(val_type) == type:
                    values = [val_type(value) for value in values]
                else:
                    values = [val_type(values)]

            if len(values) == 1:
                values = values[0]

            inp.append(values)

        if len(inp) == 1:
            return inp[0]
        return inp
