        ORG.    0x0000

start:  INP 0x0FE   # Read console input        0xE0FE
        OUT 0x0FF   # Write back to display     0xF0FF
        BRA start   # Loop                      0xB000
