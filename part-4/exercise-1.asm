# Example-1
# Write a Tiny-P assembly program to multiply two
# single digit number. Stored the result into RAM[2].
# Note: Example doesn't specify the location of the two
# numbers to be multiplied. So we will place them in
# RAM[0] and RAM[1] multiplying the former by the later.

    LDA  2     # Load ACC with value in  partial answer
    ADD  0     # Add  multplican to (partial) answer
    STA  2     # Save value in RAM[2] (answer)
    LDA  1     # Load ACC with multiplier from RAM[1]
    SUB  3     # Decrement (RAM[3] holds value 1 for decrementing)
    STA  1     # Save new count
    BRZ  6     # If count equals zero we are done!
    BRP  0     # Not done yet, so go back to beginning

# Translated to Tiny-P machine code
00 102
01 600
02 202
03 101
04 703
05 201
06 806
07 90
