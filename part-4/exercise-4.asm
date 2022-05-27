# Exercise-4 Assembly Language Program for the Tiny-P
# Write a Tiny-P assembly program to logically NOT (Invert) a single digit number and stored the result into RAM[10].
# Note: the exercise does not specify the location of the values to be NOTed.
# We will use RAM[0] to hold this values.

    LDA 0
    NOT
    STA 10


# Translation to machine code
00 100
01 500
02 210