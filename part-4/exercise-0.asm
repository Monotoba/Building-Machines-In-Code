# Exercise-0 Assembly Language Program for the Tiny-P
# Write a Tiny-P assembly program to subtract the number stored in RAM[1]
# from the number stored in RAM[0] and save the result into RAM[3]. Then
# translate that program into machine code as we did in the article.
    LDA 0
    SUB 1
    STA 3


# Translation to machine code
00 100
01 701
02 203