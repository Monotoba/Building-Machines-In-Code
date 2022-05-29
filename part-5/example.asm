# Sample Tiny-P Assembler Program
# Comments start with a hash symbol "#"

             ORG. 0     # Origin: starting address of program code
#             DATA. 20   # Data Origin, starting address of variables

             # Data statements are variables
#DAT0:        DATA 1
#DAT1         DATA 5
#SUM:         DATA 0

start:       LDA  0        # Load ACC with value stored in Mem[0]
             ADD  1        # Add value stored in Mem[1] to ACC
             STA  2        # Save result of Add in Mem[2]
             BRZ  start    # If result is zero return to start
