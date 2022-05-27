# Exercise-3 Assembly Language Program for the Tiny-P
# Write a Tiny-P assembly program to logically OR two single digit number stored the result into RAM[6].
# Note: the exercise does not specify the location of the two values to be ANDed together.
# We will use RAM[0] and RAM[1] to hold these values.

    LDA 0
    OR  1
    STA 6


# Translation to machine code
00 100
01 401
02 206