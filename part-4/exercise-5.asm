# Exercise-4 Assembly Language Program for the Tiny-P
# Write a Tiny-P assembly program to Add two single digit number
# stored in RAM[0] and RAM[1]. Then stored the result into RAM[0].
# Branch back to program address 0 using a BRP instruction. Follow
# the BRP instruction with a BRZ to the location ROM of the BRZ
# instruction. This creates an inifinte loop at this instruction,
# effectively pausing the program. Single step through this program
# using the cpu's step() method.

    LDA  0
    ADD  1
    STA  0
    BRP  0
    BRZ  4

# Translated to Tiny-P Machine Code

00 100
01 601
02 200
03 900
04 804