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
__date__ = "2022/06/08"
__deprecated__ = False
__email__ = "rmorgan@coderancher.us"
__license__ = "BSD-2-Clause"
__maintainer__ = "Randall Morgan"
__status__ = "Educational"
__version__ = "1.0.0"

import sys

from bus import BusClient


class Console(BusClient):
    BASE_ADDRESS = 0x00FE  # Read
    MAX_ADDRESS = 0x00FF  # Write

    def __init__(self, base_address: int = None, max_address: int = None):
        Console.BASE_ADDRESS = base_address if base_address is not None else 0x00FE
        Console.MAX_ADDRESS = max_address if max_address is not None else 0x00FF

    @staticmethod
    def should_respond(address, is_io_request=False):
        return Console.BASE_ADDRESS <= address <= Console.MAX_ADDRESS

    @staticmethod
    def read(address) -> int | None:
        if Console.should_respond(address):
            try:
                return ord(sys.stdin.buffer.read(1))
            except KeyboardInterrupt:
                pass
        return None

    @staticmethod
    def write(address, data):
        if Console.should_respond(address):

            char = chr(data & 0xFF)
            try:
                sys.stdout.write(char)
                sys.stdout.buffer.flush()
            except KeyboardInterrupt:
                pass


if __name__ == "__main__":
    console = Console()
    # Read the terminal window
    while True:
        ch = console.read(0x00FE)
        console.write(0x00FF, ch)
