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
