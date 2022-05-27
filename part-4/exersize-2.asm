# Exercise-2 Assembly Language Program for the Tiny-P
# Write a Tiny-P assembly program to logically AND two single digit number stored the result into RAM[9].
# Note: the exercise does not specify the location of the two values to be ANDed together.
# We will use RAM[0] and RAM[1] to hold these values.

    LDA 0
    AND 1
    STA 3


# Translation to machine code
00 100
01 301
02 209