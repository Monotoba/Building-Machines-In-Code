#!/usr/bin/python3
# Tiny-P Assembler
import sys, getopt

# The Opcode table relates mnemonics
# to the corresponding opcode value.
OPCODE_TABLE = {
    'nop': 0,
    'lda': 1,
    'sta': 2,
    'and': 3,
    'or': 4,
    'not': 5,
    'add': 6,
    'sub': 7,
    'brz': 8,
    'brp': 9
}

MNEMONICS = ['nop', 'lda', 'sta', 'and', 'or', 'not', 'add', 'sub', 'brz', 'brp']


class Lexer:
    def __init__(self):
        self.line = None
        self.tokens = []

    def set_text(self, line: str):
        self.line = line
        self.tokens = line.split()

    def next_token(self):
        if not self.tokens:
            return None

        tok = self.tokens.pop(0)
        return tok


class Assembler:
    def __init__(self, text_: str):
        self.text = text_
        self.lines = self.text.split('\n')
        self.current_address = 0
        self.opcode = 0
        self.operand = 0
        self.lexer = Lexer()
        self.symbol_table = {}
        self.code = []

    def skip_spaces(self, tok: str):
        while tok.isspace():
            tok = self.lexer.next_token()

    def skip_comment(self, tok: str):
        if tok == '#':
            while tok:
                tok = self.lexer.next_token()

    def fixup(self):
        text_ = ''
        for line in self.code:
            parts = line.split(':')
            addr = parts[0]
            sub_parts = parts[1].split('-')
            opcode = sub_parts[0]
            operand = sub_parts[1]

            if operand.isalnum() and not operand.isnumeric():
                if operand in self.symbol_table:
                    operand = self.symbol_table[operand]
                else:
                    raise ValueError(f"Undefined Symbol: {operand}")

            bin_code = (int(opcode) * 100) + int(operand)
            if bin_code > 999:
                raise ValueError(f"Illegal Machine Code Value {bin_code}")
            code_line = f'{addr.zfill(4)} {bin_code}\n'
            text_ += code_line

        return text_

    def parse(self):
        for line in self.lines:
            line = line.lower()
            self.opcode = 0
            self.operand = 0

            self.lexer.set_text(line)

            tok = self.lexer.next_token()
            while tok is not None:
                self.skip_spaces(tok)

                if tok is None or not tok:
                    break

                elif tok.endswith(':'):
                    # LABEL_DECL
                    key = tok[:-1]
                    self.symbol_table[key] = self.current_address

                elif tok == '#':
                    # COMMENT
                    self.skip_comment(tok)
                    break

                elif tok.endswith('.'):
                    # DIRECTIVE
                    if tok[:-1] == 'org':
                        operand = self.lexer.next_token()
                        if operand.isnumeric():
                            self.current_address = int(operand)
                        else:
                            raise ValueError('Illegal Origin. Expected: integer, Found {operand}')
                    break
                elif tok in MNEMONICS:
                    # INSTRUCTION
                    self.opcode = OPCODE_TABLE[tok]
                    operand = self.lexer.next_token()
                    if operand.isnumeric():
                        self.operand = operand
                    elif operand.isalnum():
                        if operand in self.symbol_table:
                            self.operand = self.symbol_table[operand]
                        else:
                            self.operand = operand
                    elif operand.startswith('#'):
                        self.operand = 0
                        self.skip_comment(operand)

                    self.code.append(f"{self.current_address} : {self.opcode}-{self.operand}")
                    self.current_address += 1

                tok = self.lexer.next_token()

        code_text = self.fixup()

        return code_text


def main(argv):
    inputfile = ''
    outputfile = ''
    usage_message = "Usage: assembler.py -i <inputfile> -o <outputfile>"

    try:
        opts, args = getopt.getopt(argv, "hi:0:", ["help", "ifile=", "ofile="])
    except getopt.GetoptError:
        print(usage_message)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage_message)
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg

    if not inputfile:
        print(usage_message)
        sys.exit(2)

    # If only input file given default output file to <inputfile>.bin
    if inputfile and not outputfile:
        outputfile = inputfile.split('.')[0]
        outputfile += '.bin'

    with open(inputfile, 'r') as ifh:
        program_text = ifh.read()
    ifh.close()

    # Assemble program
    assembler = Assembler(program_text)
    machine_text = assembler.parse()

    # Write output file
    with open(outputfile, 'w') as ofh:
        ofh.write(machine_text)
    ofh.close()

    # Exit message
    print(f"Assembled: {inputfile} and wrote machine code to {outputfile}")


if __name__ == '__main__':
    main(sys.argv[1:])
