#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSD-2-Clause
""" Tiny-T CPU Simulator.
Tiny-T is a simple CPU Simulator intended as a teaching aid for students
learning about computer architecture.
Released under the BSD 2-Clause License. See the repository LICENSE file.
Copyright and attribution notices must be retained in redistributions.
"""

__author__ = "Randall Morgan"
__contact__ = "rmorgan@coderancher.us"
__copyright__ = "Copyright 2022, SensorNet"
__credits__ = ["Randall Morgan", "SensorNet.Us"]
__date__ = "2022/05/23"
__deprecated__ = False
__email__ = "rmorgan@coderancher.us"
__license__ = "BSD-2-Clause"
__maintainer__ = "Randall Morgan"
__status__ = "Educational"
__version__ = "1.0.0"

# Tiny-T Machine Code Loader
# Assumes machine code is stored in
# a *.bin file and is formatted as:
# <address> <opcode>
# Where the address is a 4-digit decimal
# value and the opcode is a 4-digit
# decimal value.

import getopt
import sys

from bus import Bus
from console import Console
from cpu import CPU
from memory import Memory


class Loader:
    def __init__(self, cpu: CPU, code_text: str):
        self.machine_code = code_text
        self.code = self.machine_code.split('\n')
        self.cpu = cpu

    def load(self):
        for line in self.code:
            code = line.split()
            if len(code) == 2:
                addr = int(code[0])
                opcode = int(code[1])
                self.cpu.write(addr, opcode)


def dump(cpu: CPU):
    print(f"ACC: {cpu.accumulator}, PC: {cpu.program_counter}, Z: {cpu.z_flag}, P: {cpu.p_flag}")
    print('\n')


def dump_mem(mem: list):
    for i, data in enumerate(mem):
        if i % 16 == 0: print(f"\n{i} : ", end='')
        print(f" {data}, ", end='')
    print()


def main(argv):
    inputfile = ''
    usage_message = "Usage: assembler.py -i <inputfile> "

    try:
        opts, args = getopt.getopt(argv, "hi:", ["help", "ifile="])
    except getopt.GetoptError:
        print(usage_message)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage_message)
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg

    if not inputfile:
        print(usage_message)
        sys.exit(2)

    with open(inputfile, 'r') as ifh:
        program_text = ifh.read()
    ifh.close()

    # Build up Computer Stem
    ram = Memory(64, 16)
    con = Console()
    bus = Bus()
    bus.register_handler(ram)
    bus.register_handler(con)
    cpu = CPU(bus)

    # Loader Program
    loader = Loader(cpu, program_text)
    loader.load()

    # Exit message
    print(f"Loader: {inputfile} loaded in to cpu.")
    print(f"Ready to run!")

    # Run the program
    cpu.run()


if __name__ == "__main__":
    main(sys.argv[1:])
