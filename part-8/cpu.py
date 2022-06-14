#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Tiny-T CPU Simulator.
Tiny-T is a simple CPU Simulator intended as a teaching aid for students
learning about computer architecture.
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 2 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR ANY PARTICULAR PURPOSE. See the GNU General Public License for more details.
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

import time

from bus import Bus

class CPU:

    def __init__(self, bus: Bus):
        self.accumulator = 0
        self.program_counter = 0
        self.instruction_register = 0
        self.address_register = 0
        self.z_flag = 0
        self.p_flag = 0
        self.bus = bus
        self.active = True

    def set_accumulator(self, value):
        # Set Zero flag
        if value == 0:
            self.z_flag = True
        else:
            self.z_flag = False

        # Set Positive flag
        if value & 0b1000_0000_0000_0000:
            self.p_flag = False
        else:
            self.p_flag = True

        # Write value into accumulator
        self.accumulator = value & 0xFFFF

    def bus_read(self, address) -> int:
        return self.bus.read(address)

    def bus_write(self, address, value):
        self.bus.write(address, value)

    def fetch(self, address: int):
        address = address & 0xFFF
        result = self.bus_read(address)
        return result

    def write(self, address: int, value: int):
        self.bus_write(address, value)

    def decode(self, instr) -> tuple[int, int]:
        # Split opcode and operand
        return (instr & 0xF000) >> 12, instr & 0x0FFF

    def step(self):
        self.instruction_register = self.fetch(self.program_counter)
        self.program_counter += 1
        opcode, operand = self.decode(self.instruction_register)
        self.execute(opcode, operand)

    def run(self):
        while self.active:
            self.step()
            #time.sleep(0.02)

    def execute(self, opcode, operand):
        match (opcode):
            case 0x0:
                self.__impl_halt()
            case 0x1:
                self.__impl_load(operand)
            case 0x2:
                self.__impl_store(operand)
            case 0x3:
                self.__impl_add(operand)
            case 0x4:
                self.__impl_sub(operand)
            case 0x5:
                self.__impl_and(operand)
            case 0x6:
                self.__impl_or(operand)
            case 0x7:
                self.__impl_xor(operand)
            case 0x8:
                self.__impl_not()
            case 0x9:
                self.__impl_shift_left()
            case 0xA:
                self.__impl_shift_right()
            case 0xB:
                self.__impl_branch_always(operand)
            case 0xC:
                self.__impl_branch_positive(operand)
            case 0xD:
                self.__impl_branch_zero(operand)
            case 0xE:
                self.__impl_input(operand)
            case 0xF:
                self.__impl_output(operand)
            case _:
                raise ValueError(f"Illegal opcode: {opcode}")

    def __impl_halt(self):
        self.active = False

    def __impl_load(self, operand: int):
        self.set_accumulator(self.fetch(operand))

    def __impl_store(self, operand: int):
        self.write(operand, self.accumulator)

    def __impl_add(self, operand: int):
        value = self.fetch(operand)
        _sum = self.accumulator + value
        self.set_accumulator(_sum)

    def __impl_sub(self, operand: int):
        value = self.fetch(operand)
        diff = self.accumulator - value
        self.set_accumulator(diff)

    def __impl_and(self, operand: int):
        value = self.fetch(operand)
        result = self.accumulator & value
        self.set_accumulator(result)

    def __impl_or(self, operand: int):
        value = self.fetch(operand)
        result = self.accumulator | value
        self.set_accumulator(result)

    def __impl_xor(self, operand: int):
        value = self.fetch(operand)
        result = self.accumulator ^ value
        self.set_accumulator(result)

    def __impl_not(self):
        result = ~self.accumulator
        self.set_accumulator(result)

    def __impl_shift_left(self):
        result = self.accumulator >> 1
        self.set_accumulator(result)

    def __impl_shift_right(self):
        result = self.accumulator << 1
        self.set_accumulator(result)

    def __impl_branch_always(self, operand: int):
        self.program_counter = operand

    def __impl_branch_positive(self, operand: int):
        if self.p_flag:
            self.program_counter = operand

    def __impl_branch_zero(self, operand: int):
        if self.z_flag:
            self.program_counter = operand

    def __impl_input(self, operand: int):
        # IO operations must set bus io request flag
        # or the following read/write operations will
        # be interpreted as a memory address space
        # operation.
        self.bus.set_io_request()
        b = (self.bus_read(0xFE) & 0xFF).to_bytes(1)
        ch = ord(b)
        self.set_accumulator(ch)
        self.bus.clear_io_request()

    def __impl_output(self, operand: bytes):
        # IO operations must set bus io request flag
        # or the following read/write operations will
        # be interpreted as a memory address space
        # operation.
        self.bus.set_io_request()
        ch = self.accumulator
        self.bus_write(0xFF, ch)
        self.bus.clear_io_request()
