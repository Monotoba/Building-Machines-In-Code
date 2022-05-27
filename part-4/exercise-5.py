# Building Machines In Code - Part 4
# Tiny-P Programming Exercise 5
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
        print("01    ADD  1")
        cpu.step()
        print("02    STA  0")
        cpu.step()
        print("03    BRP  0")
        cpu.step()
        #print("04    BRZ  4")
        print("--- Loop ---")
        iterations -= 1

def main(cpu=None, iterations=1):
    #

    # Initialize the CPU
    cpu.init_rom()
    cpu.reset()

    # Setup data values in RAM
    cpu.mem[0] = 0      # 0 + 3
    cpu.mem[1] = 3
    cpu.mem[10] = 0

    # Program the ROM
    cpu.program(0, 100)     # LDA 0
    cpu.program(1, 601)     # ADD 1
    cpu.program(2, 200)     # STA 0
    cpu.program(3, 900)     # BRP 0
    cpu.program(4, 804)     # BRZ 4

    # Run the program
    cpu.debug = True
    program_iterations(cpu, iterations)



if __name__ == "__main__":
    # Instantiate the CPU
    cpu = CPU()
    main(cpu, 4)