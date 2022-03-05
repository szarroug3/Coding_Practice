#!/usr/bin/env python3

import argparse
from dis import disassemble
from re import S
import traceback
import os

MOD_VALUE = 32768
DEBUG = True


class VirtualMachineException(Exception):
    pass


class VirtualMachine:
    def __init__(self, binary):
        self.registers = [0] * 8
        self.registers[7] = 1
        self.stack = []
        self.index = 0
        self.done = False
        self.input = ""
        self.print_save_newline = True
        self.print_input = False
        self.read_binary_file(binary)

    def read_binary_file(self, filename):
        if not os.path.exists(filename):
            filename = os.path.join(os.path.dirname(
                os.path.realpath(__file__)), filename)

        if not os.path.exists(filename):
            raise VirtualMachineException(
                f'The file, {filename}, doesn\'t exist')

        self.data = [0] * 32767
        index = 0
        with open(filename, 'rb') as f:
            while True:
                byte = f.read(2)
                if not byte:
                    break
                self.data[index] = int.from_bytes(byte, "little")
                index += 1

    def read_save_file(self, filename):
        if not os.path.exists(filename):
            filename = os.path.join(os.path.dirname(
                os.path.realpath(__file__)), filename)

        if not os.path.exists(filename):
            return

        with open(filename) as f:
            self.input = f.read()

        if len(self.input) > 0 and self.input[-1] != '\n':
            self.input += '\n'
            self.print_input = True

    def setup_output_file(self, filename):
        if not os.path.exists(filename):
            filename = os.path.join(os.path.dirname(
                os.path.realpath(__file__)), filename)

        if os.path.exists(filename):
            os.remove(filename)

        self.output = filename

    def memory_hack(self):
        self.data[521] = 21
        self.data[522] = 21
        self.data[523] = 21

    def disassemble(self, filename):
        if not os.path.exists(filename):
            filename = os.path.join(os.path.dirname(
                os.path.realpath(__file__)), filename)

        func_data = [
            ['halt', 0], ['set', 2], ['push', 1], ['pop',  1],
            ['eq',  3], ['gt',  3], ['jmp',  1], ['jt',  2],
            ['jf',  2], ['add',  3], ['mult',  3], ['mod',  3],
            ['and',  3], ['or',  3], ['not',  2], ['rmem',  2],
            ['wmem',  2], ['call',  1], ['ret', 0], ['out',  1],
            ['in',  1], ['noop', 0],
        ]

        with open(filename, 'w') as f:
            index = 0
            while index < len(self.data):
                f.write('{}: '.format(index))
                if self.data[index] < len(func_data):
                    opcode, count = func_data[self.data[index]]
                    index += 1
                    f.write(opcode)
                    values = []
                    for _ in range(count):
                        curr = self.data[index]
                        if 32768 <= curr <= 32775:
                            values.append('${}'.format(curr % MOD_VALUE))
                        else:
                            values.append(str(curr))
                        index += 1
                    if values:
                        f.write(' {}'.format(' '.join(values)))
                else:
                    f.write(str(self.data[index]))
                    index += 1
                f.write('\n')

    def execute(self, save, output):
        opcodes = {
            0: self.halt, 1: self.set, 2: self.push, 3: self.pop, 4: self.eq, 5: self.gt,
            6: self.jmp, 7: self.jt, 8: self.jf, 9: self.add, 10: self.mult, 11: self.mod,
            12: self.bitwise_and, 13: self.bitwise_or, 14: self.bitwise_not, 15: self.rmem,
            16: self.wmem, 17: self.call, 18: self.ret, 19: self.out, 20: self.read, 21: self.noop
        }
        self.read_save_file(save)
        self.setup_output_file(output)
        self.memory_hack()

        disassembled = {}
        with open('disassembled.asm') as f:
            curr = f.readline().strip()
            while curr:
                curr = curr.split(' ')
                if len(curr) < 5:
                    curr.extend([''] * (5-len(curr)))
                disassembled[int(curr[0][:-1])] = ' '.join(value.rjust(5)
                                                           for value in curr[1:])
                curr = f.readline().strip()

        os.remove('log.txt')
        self.count = 0
        while not self.done:
            if self.count > 922456:
                with open('log.txt', 'a') as f:
                    line = str(self.index).rjust(5)
                    line += ' '
                    line += disassembled[self.index]
                    line += ' ['
                    line += ' '.join(str(register).rjust(5)
                                     for register in self.registers)
                    line += '] ['
                    line += ' '.join(str(item).rjust(5) for item in self.stack)
                    line += ']'
                    print(line, end='')
                    f.write(line + '\n')
                input()
            if self.index >= len(self.data):
                raise VirtualMachineException('Invalid index')

            opcode = self.get_value()
            self.count += 1
            self.index += 1
            opcodes[opcode]()
            self.index += 1

    def get_value(self, get_from_register=False):
        value = self.data[self.index]

        if value > 32775:
            raise VirtualMachineException('Invalid value')

        if value > 32767:
            value = value % MOD_VALUE
            if get_from_register:
                return self.registers[value]

        return value

    def halt(self):
        """
        halt: 0
            stop execution and terminate the program
        """
        self.done = True

    def set(self):
        """
        set: 1 a b
            set register <a> to the value of <b>
        """
        a = self.get_value()
        self.index += 1
        b = self.get_value(get_from_register=True)

        self.registers[a] = b

    def push(self):
        """
        push: 2 a
            push <a> onto the stack
        """
        a = self.get_value(get_from_register=True)
        self.stack.append(a)

    def pop(self):
        """
        pop: 3 a
            remove the top element from the stack and write it into <a>; empty stack = error
        """
        if len(self.stack) == 0:
            raise VirtualMachineException(
                "Error: trying to pop from empty stack")

        a = self.get_value()
        self.registers[a] = self.stack.pop()

    def eq(self):
        """
        eq: 4 a b c
            set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise
        """
        a = self.get_value()
        self.index += 1
        b = self.get_value(get_from_register=True)
        self.index += 1
        c = self.get_value(get_from_register=True)

        if b == c:
            self.registers[a] = 1
        else:
            self.registers[a] = 0

    def gt(self):
        """
        gt: 5 a b c
            set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
        """
        a = self.get_value()
        self.index += 1
        b = self.get_value(get_from_register=True)
        self.index += 1
        c = self.get_value(get_from_register=True)

        if b > c:
            self.registers[a] = 1
        else:
            self.registers[a] = 0

    def jmp(self, destination=None):
        """
        jmp: 6 a
            jump to <a>
        """
        if not destination:
            destination = self.get_value(get_from_register=True)
        self.index = destination - 1

    def jt(self):
        """
        jt: 7 a b
            if <a> is nonzero, jump to <b>
        """
        a = self.get_value(get_from_register=True)
        self.index += 1

        if a:
            self.jmp()

    def jf(self):
        """
        jf: 8 a b
            if <a> is zero, jump to <b>
        """
        a = self.get_value(get_from_register=True)
        self.index += 1

        if not a:
            self.jmp()

    def add(self):
        """
        add: 9 a b c
            assign into <a> the sum of <b> and <c> (modulo 32768)
        """
        a = self.get_value()
        self.index += 1
        b = self.get_value(get_from_register=True)
        self.index += 1
        c = self.get_value(get_from_register=True)

        self.registers[a] = (b + c) % MOD_VALUE

    def mult(self):
        """
        mult: 10 a b c
            store into <a> the product of <b> and <c> (modulo 32768)
        """
        a = self.get_value()
        self.index += 1
        b = self.get_value(get_from_register=True)
        self.index += 1
        c = self.get_value(get_from_register=True)

        self.registers[a] = (b * c) % MOD_VALUE

    def mod(self):
        """
        mod: 11 a b c
            store into <a> the remainder of <b> divided by <c>
        """
        a = self.get_value()
        self.index += 1
        b = self.get_value(get_from_register=True)
        self.index += 1
        c = self.get_value(get_from_register=True)

        self.registers[a] = b % c

    def bitwise_and(self):
        """
        and: 12 a b c
            stores into <a> the bitwise and of <b> and <c>
        """
        a = self.get_value()
        self.index += 1
        b = self.get_value(get_from_register=True)
        self.index += 1
        c = self.get_value(get_from_register=True)

        valueB = bin(b)[2:].rjust(15, '0')
        valueC = bin(c)[2:].rjust(15, '0')

        value = ""
        for i in range(len(valueB)):
            if valueB[i] == '1' and valueC[i] == '1':
                value += '1'
            else:
                value += '0'

        self.registers[a] = int(value, 2)

    def bitwise_or(self):
        """
        or: 13 a b c
            stores into <a> the bitwise or of <b> and <c>
        """
        a = self.get_value()
        self.index += 1
        b = self.get_value(get_from_register=True)
        self.index += 1
        c = self.get_value(get_from_register=True)

        valueB = bin(b)[2:].rjust(15, '0')
        valueC = bin(c)[2:].rjust(15, '0')

        value = ""
        for i in range(len(valueB)):
            if valueB[i] == '1' or valueC[i] == '1':
                value += '1'
            else:
                value += '0'

        self.registers[a] = int(value, 2)

    def bitwise_not(self):
        """
        not: 14 a b
            stores 15-bit bitwise inverse of <b> in <a>
        """
        a = self.get_value()
        self.index += 1
        b = self.get_value(get_from_register=True)

        value = bin(b)[2:].rjust(15, '0')
        value = ''.join(['0' if letter == '1' else '1' for letter in value])
        self.registers[a] = int(value, 2)

    def rmem(self):
        """
        rmem: 15 a b
            read memory at address <b> and write it to <a>
        """
        a = self.get_value()
        self.index += 1
        b = self.get_value(get_from_register=True)

        self.registers[a] = self.data[b]

    def wmem(self):
        """
        wmem: 16 a b
            write the value from <b> into memory at address <a>
        """
        a = self.get_value(get_from_register=True)
        self.index += 1
        b = self.get_value(get_from_register=True)

        self.data[a] = b

    def call(self):
        """
        call: 17 a
            write the address of the next instruction to the stack and jump to <a>
        """
        self.stack.append(self.index+1)
        self.jmp()

    def ret(self):
        """
        ret: 18
            remove the top element from the stack and jump to it; empty stack = halt
        """
        if len(self.stack) == 0:
            self.halt()
        else:
            self.jmp(destination=self.stack.pop())

    def out(self):
        """
        out: 19 a
            write the character represented by ascii code <a> to the terminal
        """
        a = self.get_value(get_from_register=True)
        print(chr(a), end='')

    def read(self):
        """
        in: 20 a
            read a character from the terminal and write its ascii code to <a>; it can be assumed that once input starts, it will continue until a newline is encountered; this means that you can safely read whole lines from the keyboard and trust that they will be fully read
        """
        a = self.get_value()

        if len(self.input) == 0:
            self.print_input = False
            self.input = input('> ') + '\n'
            with open(self.output, 'a') as f:
                f.write(self.input)
        elif self.print_input:
            if self.print_save_newline:
                print('> ', end='')
                self.print_save_newline = False

            if self.input[0] == '\n':
                self.print_save_newline = True

            print(self.input[0], end='')

        self.registers[a] = ord(self.input[0])
        self.input = self.input[1:]

    def noop(self):
        """
        noop: 21
            no operation
        """
        # subtract 1 to account for execute adding one when we don't need to
        self.index -= 1


def parse_args():
    parser = argparse.ArgumentParser(
        description='Run a synacore virtual machine')
    parser.add_argument('--binary', '-b', default='challenge.bin',
                        help='the binary to run')
    parser.add_argument('--save', '-s', default='save.txt',
                        help='the save file to start with')
    parser.add_argument('--output', '-o', default='output.txt',
                        help='the output file to write path taken to')
    parser.add_argument('--disassemble', '-d',
                        help='create a disassembled file and save it to input argument')
    return parser.parse_args()


def main():
    try:
        args = parse_args()
        vm = VirtualMachine(args.binary)
        if args.disassemble:
            vm.disassemble(args.disassemble)
        else:
            vm.execute(args.save, args.output)
    except Exception as e:
        if DEBUG:
            traceback.print_exc()
        else:
            print(e)


if __name__ == '__main__':
    main()
