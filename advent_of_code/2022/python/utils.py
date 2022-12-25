# !/bin/python3

import inspect
import os
import sys


def get_filename(fname, sample, parent):
    if fname:
        return fname

    if len(sys.argv) == 2:
        return sys.argv[1]

    if not parent:
        frame = inspect.stack()[2]
        parent = frame[0].f_code.co_filename

    if sample:
        return '{0}sample{1}.txt'.format(os.path.splitext(parent)[0], sample)
    return '{0}input.txt'.format(os.path.splitext(parent)[0])


def split_line(line, line_delimiter):
    if line_delimiter:
        return line.split(line_delimiter)
    if line_delimiter == "":
        return list(line)
    return line


def strip_values(values, ignore_empty):
    if not ignore_empty:
        return values
    if type(values) is list:
        return [value.strip() for value in values if value]
    return values.strip()


def convert_values(values, val_type):
    if not val_type:
        return values

    if type(values) is list:
        if type(val_type) is list:
            conversions = zip(val_type, values)
            return [t(value) if t else value for t, value in conversions]
        return [val_type(value) for value in values]
    return [val_type(values)]


def read_input(
    val_type=None,
    delimiter="\n",
    line_delimiter=None,
    ignore_empty=True,
    fname=None,
    keep_single_item_list=False,
    sample=None,
    parent=None,
):
    fname = get_filename(fname, sample, parent)

    if not os.path.exists(fname):
        print(f"File {fname} doesn't exist")
        return

    with open(fname) as f:
        inp = []
        for line in f.read().split(delimiter):
            if ignore_empty and line == "":
                continue

            values = split_line(line, line_delimiter)
            values = strip_values(values, ignore_empty)
            values = convert_values(values, val_type)

            if len(values) == 1 and not keep_single_item_list:
                values = values[0]

            inp.append(values)

        if len(inp) == 1:
            return inp[0]
        return inp
