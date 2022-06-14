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

from abc import ABC


class BusClient(ABC):
    @staticmethod
    def should_respond(address, is_io_request=False):
        pass

    @staticmethod
    def read(address: int) -> int:
        pass

    @staticmethod
    def write(address: int, data: int):
        pass


class Bus:
    def __init__(self):
        self.data = 0
        self.address = 0
        self.handlers = []
        self.is_io_request = False

    def register_handler(self, handler: BusClient):
        self.handlers.append(handler)

    def set_io_request(self):
        self.is_io_request = True

    def clear_io_request(self):
        self.is_io_request = False

    def read(self, address):
        if self.is_io_request:
            address = address & 0xFF
        self.data = None
        self.address = address
        for handler in self.handlers:
            if handler.should_respond(address, self.is_io_request):
                self.data = handler.read(address)
        return self.data

    def write(self, address, data):
        if self.is_io_request:
            address = address & 0xFF
        self.data = data
        self.address = address
        for handler in self.handlers:
            if handler.should_respond(address, self.is_io_request):
                handler.write(address, data)
