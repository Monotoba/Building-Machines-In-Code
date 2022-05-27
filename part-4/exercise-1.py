# Building Machines In Code - Part 4
# Tiny-P Programming Exercise 1
#
# This program programs the Tiny-P and
# executes the code in the Tiny-P
# processor.

# Import our CPU
from cpu import CPU

def program_iterations(cpu=None, iterations=1):

    while iterations > 0:
        cpu.step()
        print("00    LDA  2")
        cpu.step()
        print("01    ADD  0")
        cpu.step()
        print("02    STA  2")
        cpu.step()
        print("03    LDA  1")
        cpu.step()
        print("04    SUB  3")
        cpu.step()
        print("05    STA  1")
        cpu.step()
        print("06    BRZ  6")
        cpu.step()
        print("07    BRP  0")
        print("--- Loop ---")
        iterations -= 1

def main(cpu=None, iterations=1):
    #

    # Initialize the CPU
    cpu.init_rom()
    cpu.reset()

    # Setup data values in RAM
    cpu.mem[0] = 5
    cpu.mem[1] = 6
    cpu.mem[2] = 0
    cpu.mem[3] = 1

    # Program the ROM
    cpu.program(0, 102)
    cpu.program(1, 600)
    cpu.program(2, 202)
    cpu.program(3, 101)
    cpu.program(4, 703)
    cpu.program(5, 201)
    cpu.program(6, 806)
    cpu.program(7, 900)

    # Run the program
    cpu.debug = True
    program_iterations(cpu, iterations)



if __name__ == "__main__":
    # Instantiate the CPU
    cpu = CPU()
    main(cpu, 20)