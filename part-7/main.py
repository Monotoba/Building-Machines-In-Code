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

from cpu import CPU
from memory import Memory
from bus import Bus


if __name__ == '__main__':
    # Instantiate System Bus Object
    bus = Bus()

    # Create System Memory
    ram = Memory(32, 16)
    ram.clear()
    ram.set_location(0x000)

    # Register Memory on bus
    bus.register_handler(ram)

    # Instantiate CPU and attach to bus
    cpu = CPU(bus)

    # Program
    cpu.write(0x0000, 0x1001)  # LDA (0x0001)
    cpu.write(0x0001, 0x00FF)  # DATA
    cpu.write(0x0002, 0x0000)  # HLT (HALT)

    # Execute
    cpu.step()  # LDA (0x0001)
    cpu.step()  # DATA
    cpu.step()  # HLT
    cpu.step()  # No effect
    cpu.step()  # No effect
