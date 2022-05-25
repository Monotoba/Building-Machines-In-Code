#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Tiny-P CPU Simulator.
Tiny-P is a simple CPU Simulator intended as a teaching aid for students
learning to about computer architecture.
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
__email__ =  "rmorgan@coderancher.us"
__license__ = "GPLv2 or Later"
__maintainer__ = "Randall Morgan"
__status__ = "Production"
__version__ = "1.0.0"

class CPU:
    def __init__(self):
        self.MAX_MEM = 100
        self.acc = 0
        self.pc = 0
        self.instr = 0
        self.zero_flag = True
        self.pos_flag = True
        self.cycle_time_in_ms = 500
        self.prog = []
        self.mem = []
        self.halted = False
        self.debug = False

    def run(self):
        while not self.halted:
            self.step()

    def step(self):
        self.fetch()
        self.decode()
        if self.debug:
            self.trace()

    def halt(self):
        self.halted = True

    def trace(self):
        # Display CPU and Memory
        print(f'Opcode: {self.opcode}, Operand: {self.operand}')
        print(f"ACC: {self.acc}, PC: {self.pc}, Z: {self.zero_flag}, P: {self.pos_flag}")
        print(f"ROM: {self.prog}")
        print(f"MEM: {self.mem}")

    def cold_start(self):
        self.init_rom()

    def reset(self):
        self.acc = self.pc = self.instr = 0
        self.zero_flag = self.pos_flag = True
        self.init_memory()

    def update_acc(self, value):
        # Update CPU Accumulator and flags
        self.acc = value
        self.update_status()

    def update_pc(self, value):
        self.pc = value

    def update_status(self):
        # Update CPU status flags
        self.zero_flag = self.acc == 0
        self.pos_flag = self.acc >= 0

    def init_rom(self):
        # Initialize all ROM to zero
        for i in range(self.MAX_MEM):
            self.prog.append(0)

    def init_memory(self):
        # Initialize all memory to zero
        for i in range(self.MAX_MEM):
            self.mem.append(0)

    def read_memory(self, address):
        # Return the value stored in memory at <address>
        return self.mem[address]

    def write_memory(self, address, value):
        # Write <value> to memory location <address>
        self.mem[address] = value

    def read_prog(self, address):
        # Return an instruction from ROM location <address>
        return self.prog[address]

    def program(self, address, value):
        # Program the ROM location <address> with the value <value>
        self.prog[address] = value

    def test_opcode(self, expected):
        if self.opcode != expected:
            raise ValueError(f"Illegal Opcode, expected: {expected} Got: {self.opcode}")
        return

    def test_operand(self):
        if self.operand >= 100:
            raise ValueError(f"Illegal Operand, expected: 0 - 99 Got: {self.operand}")
        return

    # Instruction Cycle methods
    def fetch(self):
        # Fetch an instruction and increment the pc
        self.instr = self.read_prog(self.pc)
        self.pc += 1
        if self.pc >= self.MAX_MEM:
            self.pc = 0

    def decode(self):
        # Decode instruction value into opcode and address/data values
        if self.instr in range(0, 100, 1):
            self.opcode = 0
            self.operand = self.instr
            self.nop()

        elif self.instr in range(100, 200):
            self.opcode = 1
            self.operand = self.instr - 100
            self.lda()

        elif self.instr in range(200, 300):
            self.opcode = 2
            self.operand = self.instr - 200
            self.sta()

        elif self.instr in range(300, 400):
            self.opcode = 3
            self.operand = self.instr - 300
            self.and_()

        elif self.instr in range(400, 500):
            self.opcode = 4
            self.operand = self.instr - 400
            self.or_()

        elif self.instr in range(500, 600):
            self.opcode = 5
            self.operand = self.instr - 500
            self.not_()

        elif self.instr in range(600, 700):
            self.opcode = 6
            self.operand = self.instr - 600
            self.add()

        elif self.instr in range(700, 800):
            self.opcode = 7
            self.operand = self.instr - 700
            self.sub()

        elif self.instr in range(800, 900):
            self.opcode = 8
            self.operand = self.instr - 800
            self.brz()

        elif self.instr in range(900, 1000):
            self.opcode = 9
            self.operand = self.instr - 900
            self.brp()

        else:
            raise ValueError("Undefined Opcode")

    # Instruction execution methods
    def nop(self):
        # NOP - No Operation
        if not self.opcode == 0:
            raise ValueError(f"Illegal Opcode, expected: 0 got: {self.opcode}")
        return

    def lda(self):
        self.test_opcode(1)
        self.test_operand()
        self.update_acc(self.read_memory(self.operand))

    def sta(self):
        # Store the of the ACC in memory location <operand>
        self.test_opcode(2)
        self.test_operand()
        self.write_memory(self.operand, self.acc)

    def and_(self):
        # Logically AND the value in ACC and memory location <operand>
        # and place the results back in ACC, then set the status flags
        # accordingly
        self.test_opcode(3)
        self.test_operand()
        value = self.read_memory(self.operand)
        self.update_acc(self.acc & value)

    def or_(self):
        # Logically OR the value in ACC and memory location <operand>
        # and place the results back in ACC, then set the status flags
        # accordingly
        self.test_opcode(4)
        self.test_operand()
        value = self.read_memory(self.operand)
        self.update_acc(self.acc | value)

    def not_(self):
        # Logically NOT the value in ACC and place the
        # results back in ACC, then set the status flags
        # accordingly
        self.test_opcode(5)
        self.test_operand()
        self.update_acc(not self.acc)

    def add(self):
        # ADD the value in ACC to the value in memory location <operand>
        # and place the results back in ACC, then set the status flags
        # accordingly
        self.test_opcode(6)
        self.test_operand()
        value = self.read_memory(self.operand)
        self.update_acc(self.acc + value)

    def sub(self):
        # SUBTRACT the value in ACC from the value in memory location <operand>
        # and place the results back in ACC, then set the status flags accordingly
        self.test_opcode(7)
        self.test_operand()
        value = self.read_memory(self.operand)
        self.update_acc(self.acc - value)


    def brz(self):
        # IFF the last operation left the Zero flag set,
        # branch to program location <operand>. Note this
        # instruction does not alter any status flags.
        self.test_opcode(8)
        self.test_operand()
        if self.zero_flag:
            self.update_pc(self.operand)

    def brp(self):
        # IFF the last operation left the Positive flag set,
        # branch to program location <operand>. Note this
        # instruction does not alter any status flags.
        self.test_opcode(9)
        self.test_operand()
        if self.pos_flag:
            self.update_pc(self.operand)


def main():
    cpu = CPU()     # Create the CPU object

    # Test LDA
    cpu.init_rom()
    cpu.reset()      # Reset must be called before any memory access
    cpu.mem[2] = 7   # Store data to load into Accumulator
    cpu.mem[3] = 10  # Store data to AND with Accumulator
    cpu.program(0, 102)  # Program ROM (Program memory) location 0 to contain the LDA 2 instruction
    cpu.program(1, 201)  # Program ROM location 1 to contain the STA 1 instruction
    cpu.program(2, 303)  # Program ROM location 2 to contain the AND 3 instruction
    cpu.program(3, 900)  # Program ROM location 3 to contain the BRP 0 instruction
    cpu.debug = True
    cpu.run()




if __name__ == '__main__':
    main()
