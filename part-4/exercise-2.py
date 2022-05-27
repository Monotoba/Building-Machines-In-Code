# Building Machines In Code - Part 4
# Tiny-P Programming Exercise 2
#
# This program programs the Tiny-P and
# executes the code in the Tiny-P
# processor.

# Import our CPU
from cpu import CPU

def program_iterations(cpu=None, iterations=1):

    while iterations > 0:
        cpu.step()
        print("00    LDA  0")
        cpu.step()
        print("01    AND  1")
        cpu.step()
        print("02    STA  9")
        print("--- Loop ---")
        iterations -= 1

def main(cpu=None, iterations=1):
    #

    # Initialize the CPU
    cpu.init_rom()
    cpu.reset()

    # Setup data values in RAM
    cpu.mem[0] = 4      # 4 & 6 = 4
    cpu.mem[1] = 6
    cpu.mem[9] = 0

    # Program the ROM
    cpu.program(0, 100)     # LDA 0
    cpu.program(1, 301)     # AND 1
    cpu.program(2, 209)     # STA 9

    # Run the program
    cpu.debug = True
    program_iterations(cpu, iterations)



if __name__ == "__main__":
    # Instantiate the CPU
    cpu = CPU()
    main(cpu, 1)