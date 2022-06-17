#!/usr/bin/python3
# -*- coding: utf-8 -*-
# File: assembler.py
""" Tiny-T Assembler
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


# Opcode table relates mnemonics
# to the corresponding opcode value.
OPCODE_TABLE = {
    'htl': 0x0,
    'lda': 0x1,
    'sta': 0x2,
    'add': 0x3,
    'sub': 0x4,
    'and': 0x5,
    'or': 0x6,
    'xor': 0x7,
    'not': 0x8,
    'shl': 0x9,
    'shr': 0xA,
    'bra': 0xB,
    'brp': 0xC,
    'brz': 0xD,
    'inp': 0xE,
    'out': 0xF
}


class Lexer:
    def __init__(self):
        self.line = None
        self.tokens = []

    def set_text(self, line: str):
        self.line = line
        self.tokens = line.split()

    def next_token(self):
        if not self.tokens:
            return None
        tok = self.tokens.pop(0)
        return tok


class Assembler:
    def __init__(self, lexer: Lexer, _text: str):
        self.text = _text
        self.lines = self.text.split('\n')
        self.current_address = 0
        self.opcode = 0
        self.operand = 0
        self.lexer = lexer
        self.symbol_table = {}
        self.code = []

    def skip_spaces(self, tok: str):
        while tok.isspace():
            tok = self.lexer.next_token()

    def skip_comment(self, tok: str):
        if tok == '#':
            while tok:
                tok = self.lexer.next_token()

    def is_hex(self, tok: str) -> bool:
        if tok.startswith('0x') or tok.startswith('0X'):
            try:
                op = int(tok[2:], 16)
            except ValueError:
                return False
            return True
        return False

    def from_hex(self, tok: str) -> str:
        if self.is_hex(tok):
            val = str(int(tok[2:], 16))
            return val

        msg = f"Can not convert {tok} to integer value"
        raise ValueError(msg)

    def fixup(self):
        text_ = ''
        for line in self.code:
            parts = line.split(':')
            addr = parts[0]
            sub_parts = parts[1].split('-')
            opcode = sub_parts[0]
            operand = sub_parts[1]

            if operand.isalnum() and not operand.isnumeric() and not self.is_hex(operand):
                if operand in self.symbol_table:
                    operand = self.symbol_table[operand]
                else:
                    msg = f"Undefined Symbol: {operand}"
                    raise ValueError(msg)
            elif self.is_hex(operand):
                operand = self.from_hex(operand)

            bin_code = (int(opcode) << 12) + int(operand)
            if bin_code > 0xFFFF:
                raise ValueError(f"Illegal Machine Code Value {bin_code}")
            code_line = f'{addr.zfill(4)} {bin_code}\n'
            text_ += code_line

        return text_

    def parse(self):
        for line in self.lines:
            line = line.lower()
            self.opcode = 0
            self.operand = 0

            self.lexer.set_text(line)

            tok = self.lexer.next_token()
            code_text = ''
            while tok is not None:
                self.skip_spaces(tok)

                if tok is None or not tok:
                    break

                elif tok.endswith(':'):
                    # LABEL _DECL
                    key = tok[:-1]
                    self.symbol_table[key] = self.current_address

                elif tok == '#':
                    # COMMENT
                    self.skip_comment(tok)
                    break

                elif tok.endswith('.'):
                    # DIRECTIVE
                    if tok[:-1] == 'org':
                        operand = self.lexer.next_token()
                        if operand.isnumeric():
                            self.current_address = int(operand)

                        elif self.is_hex(operand):
                            try:
                                operand = int(operand[2:], 16)
                            except ValueError:
                                msg = f'Illegal value given. Expected int or hex, got {operand}'
                                raise ValueError(msg)

                        else:
                            msg = f'Illegal Origin. Expected: integer, Found {operand}'
                            raise ValueError(msg)
                        break
                elif tok in OPCODE_TABLE.keys():

                    # INSTRUCTION
                    self.opcode = OPCODE_TABLE[tok]
                    operand = self.lexer.next_token()
                    if operand.isnumeric():
                        self.operand = operand

                    elif self.is_hex(operand):
                        self.operand = self.from_hex(operand)

                    elif operand.isalnum():
                        if operand in self.symbol_table:
                            self.operand = self.symbol_table[operand]

                        elif self.is_hex(operand):
                            self.operand = self.from_hex(operand)

                        else:
                            self.operand = operand
                    elif operand.startswith('#'):
                        self.operand = 0
                        self.skip_comment(operand)

                    self.code.append(f"{self.current_address} : {self.opcode}-{self.operand}")
                    self.current_address += 1

                tok = self.lexer.next_token()

        code_text = self.fixup()

        return code_text


import getopt
import sys


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
        outputfile = inputfile.split('.')[0] + '.bin'

    with open(inputfile, 'r') as ifh:
        program_text = ifh.read()
    ifh.close()

    # Assemble program
    assembler = Assembler(Lexer(), program_text)
    machine_text = assembler.parse()

    # Write output file
    if machine_text:
        with open(outputfile, 'w') as ofh:
            ofh.write(machine_text)
        ofh.close()
    else:
        msg = f'Unable to assemble output file {inputfile}'
        raise AssertionError(msg)

    # Exit message
    print(f"Assembled: {inputfile} and wrote machine code to {outputfile}")


if __name__ == '__main__':
    main(sys.argv[1:])
