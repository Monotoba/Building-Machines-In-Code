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
__date__ = "2022/06/08"
__deprecated__ = False
__email__ = "rmorgan@coderancher.us"
__license__ = "GPLv2 or Later"
__maintainer__ = "Randall Morgan"
__status__ = "Production"
__version__ = "1.0.0"

from random import randint

from bus import BusClient


class Memory(BusClient):
    mem = []
    start_address = 0
    end_address = 4096
    bit_mask = 0

    def __init__(self, size: int, bit_width: int, read_only=False):
        self.bit_width = bit_width
        self.size = size
        self.read_only = read_only
        Memory.bit_mask = (1 << bit_width) - 1
        Memory.start_address = 0
        Memory.end_address = Memory.start_address + size
        self.clear()

    def clear(self):
        Memory.mem = [0 for _ in range(self.size)]

    def fill(self, value: int):
        Memory.mem = [value for _ in range(self.size)]

    def random_fill(self):
        Memory.mem = [(randint(0, Memory.bit_mask)) for _ in range(self.size)]

    def set_location(self, start_address: int):
        Memory.start_address = start_address
        Memory.end_address = Memory.start_address + self.size

    @staticmethod
    def should_respond(address, is_io_request=False) -> bool:
        if Memory.start_address <= address <= Memory.end_address and not is_io_request:
            return True
        return False

    @staticmethod
    def read(address: int):
        # Note during a cpu read cycle the ram puts data on the data bus
        try:
            return Memory.mem[address]
        except IndexError:
            ValueError('Address out of range or Memory not initialized')

    @staticmethod
    def write(address: int, data: int):
        # during a cpu write cycle the ram accepts data from the data bus
        Memory.mem[address] = (data & Memory.bit_mask)

    def dump(self, start_addr: int, end_addr: int) -> str:
        rep = 'Memory Dump:\n'
        for addr in range(start_addr, end_addr + 1):
            if addr % 16 == 0:
                if addr != 0:
                    rep += '\n'
                rep += ''.join(f'0x{addr:04x} : ')
            rep += ''.join(f'0x{Memory.mem[addr]:04x} ')
        return rep + '\n'

    def __str__(self) -> str:
        rep = 'Memory Dump:\n'
        for addr in range(self.size):
            if addr % 16 == 0:
                if addr != 0:
                    rep += '\n'
                rep += ''.join(f'0x{addr:04x} : ')
            rep += ''.join(f'0x{Memory.mem[addr]:04x} ')
        return rep + '\n'

    def __repr__(self) -> str:
        return self.__str__()
