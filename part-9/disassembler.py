#!/usr/bin/python3
# -*- coding: utf-8 -*-
# File: disassembler.py
""" Tiny-T Disassembler
Tiny-T is a simple CPU Simulator intended as a teaching aid for students
learning about computer architecture.
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 2 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Randall Morgan"
__contact__ = "rmorgan@coderancher.us"
__copyright__ = "Copyright 2022, SensorNet"
__credits__ = ["Randall Morgan", "SensorNet.Us"]
__date__ = "2022/05/23"
__deprecated__ = False
__email__ = "rmorgan@coderancher.us"
__license__ = "GPLv2 or Later"
__maintainer__ = "Randall Morgan"
__status__ = "Production"
__version__ = "1.0.0"

# Tiny-T CPU Instructions
# OPCODE | Mnemonic | Description
# -----------------------------------------------------
# 0xxx | HLT       | Halt
# 1xxx | LDA (xxx) | Load Acc
# 2xxx | STA (xxx) | Store A at Mem[xxx]
# 3xxx | ADD (xxx) | Add Mem[xxx] to Acc
# 4xxx | SUB (xxx) | Subtract Mem[xxx] from Acc
# 5xxx | AND (xxx) | Logical ADN ACC and Mem[xxx]
# 6xxx | OR  (xxx) | Logical OR ACC and Mem[xxx]
# 7xxx | XOR (xxx) | Logical XOR ACC and Mem[xxx]
# 8xxx | NOT       | Bitwise Invert ACC
# 9xxx | SHL       | Shift ACC left one bit
# Axxx | SHR       | Shift ACC right one bit
# Baaa | BRA aaa   | Unconditional branch to address aaa
# Caaa | BRP aaa   | Branch on positive to aaa
# Daaa | BRZ aaa   | Branch on zero to aaa
# E0pp | INP pp    | ACC <- I/O port[pp]
# F0pp | OUT pp    | I/O port[pp] <- ACC
#

import getopt
import sys


class Disassembler:
    @staticmethod
    def disasm(program_code: str):
        # Disassemble each line
        asm_text = ''
        for line in program_code.split('\n'):
            # split the address and instruction
            if line:
                addr, word = line.split()
                asm_text += f'{addr}\t\t' + Disassembler.decode(word) + '\n'
        return asm_text

    @staticmethod
    def decode(val: int) -> str:
        val = int(val)
        text = ''
        opcode = (val & 0xF000) >> 12
        operand = (val & 0x0FFF)
        mnemonic = Disassembler.INSTR[opcode].upper()
        return f'\t {mnemonic} 0x{operand:X}'

    INSTR = [
        'htl',
        'lda',
        'sta',
        'add',
        'sub',
        'and',
        'or',
        'xor',
        'not',
        'shl',
        'shr',
        'bra',
        'brp',
        'brz',
        'inp',
        'out'
    ]


def main(argv):
    inputfile = ''
    outputfile = ''
    usage_message = "Usage: assembler.py -i <inputfile> -o <outputfile>"

    try:
        opts, args = getopt.getopt(argv, "hi:0:", ["help", "ifile=", "ofile="])
    except getopt.GetoptError:
        print(usage_message)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage_message)
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg

    if not inputfile:
        print(usage_message)
        sys.exit(2)

    # If only input file given default output file to <inputfile>.bin
    if inputfile and not outputfile:
        outputfile = inputfile.split('.')[0] + '.asm_'

    with open(inputfile, 'r') as ifh:
        program_code = ifh.read()
    ifh.close()

    # Disassemble each line
    asm_text = Disassembler.disasm(program_code)

    # Write output file
    if asm_text:
        with open(outputfile, 'w') as ofh:
            ofh.write(asm_text)
        ofh.close()
    else:
        msg = f'Unable to disassemble input file {inputfile}'
        raise AssertionError(msg)


if __name__ == '__main__':
    main(sys.argv[1:])
