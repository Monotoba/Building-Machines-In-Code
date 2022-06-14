#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Tiny-T CPU Simulator.
Tiny-T is a simple CPU Simulator intended as a teaching aid for students
learning about computer architecture.
This program is free software: you can redistribute it and/or modify it under
the Terminals of the GNU General Public License as published by the Free Software
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

import sys

from bus import BusClient


class CommPort(BusClient):
    BASE_ADDRESS = 0x00FE  # Read
    MAX_ADDRESS = 0x00FF   # Write
    INSTANCE = None

    def __init__(self):
        self.input_buffer = []
        self.output_buffer = []
        CommPort.INSTANCE = self

    @staticmethod
    def should_respond(address, is_io_request=False):
        return CommPort.BASE_ADDRESS <= address <= CommPort.INSTANCE.MAX_ADDRESS

    @staticmethod
    def read(address):
        if CommPort.INSTANCE.should_respond(address):
                try:
                    return sys.stdin.buffer.read(1)
                except KeyboardInterrupt:
                    pass

        return None

    @staticmethod
    def write(address, data):
        if CommPort.INSTANCE.should_respond(address):
            #CommPort.INSTANCE.output_buffer.append(data)
            char = chr(data & 0xFF)
            try:
                sys.stdout.write(char)
                sys.stdout.buffer.flush()
            except KeyboardInterrupt:
                pass

    @staticmethod
    def write_char(char: int):
        ch = chr(char)
        CommPort.INSTANCE.input_buffer.append(ch)

    def get_buffer_char(self) -> str:
        if len(self.input_buffer):
            return str(chr(self.input_buffer.pop()))
        else:
            return ''



if __name__ == "__main__":
    pass





