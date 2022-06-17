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

from bus import Bus
from console import Console
from cpu import CPU
from memory import Memory


def dump(cpu: CPU):
    print(f'ACC: {cpu.accumulator} PC: {cpu.program_counter} P: {cpu.p_flag} Z: {cpu.z_flag}')


if __name__ == '__main__':
    # Instantiate System Bus Object
    bus = Bus()

    # Create System Memory
    ram = Memory(32, 16)
    ram.clear()
    ram.set_location(0x000)

    # Register Memory on bus
    bus.register_handler(ram)

    # Terminal
    console = Console()
    bus.register_handler(console)

    # Instantiate CPU and attach to bus
    cpu = CPU(bus)

    # Program Console Echo
    cpu.write(0x0000, 0x1004)  # LDA (0x0004)
    cpu.write(0x0001, 0xF0FF)  # OUT
    cpu.write(0x0002, 0xE0FE)  # INP
    cpu.write(0x0003, 0xB001)  # BRA 0x000
    cpu.write(0x0004, 0x0041)  # DATA = 'A'

    # Run the program
    cpu.run()
    # cpu.step()
    # dump(cpu)
    # cpu.step()
    # dump(cpu)
    # cpu.step()
    # dump(cpu)
    # cpu.step()
    # dump(cpu)
