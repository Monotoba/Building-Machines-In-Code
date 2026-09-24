# Building Machines in Code

[![CI](https://github.com/Monotoba/Building-Machines-In-Code/actions/workflows/ci.yml/badge.svg)](https://github.com/Monotoba/Building-Machines-In-Code/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: BSD-2-Clause](https://img.shields.io/badge/license-BSD--2--Clause-blue.svg)](LICENSE)
[![Project: educational](https://img.shields.io/badge/project-educational-8A2BE2.svg)](#learning-path)

Build a small computer system from first principles—with readable Python implementations
of CPUs, memory, buses, assemblers, loaders, a console device, and a disassembler.

This repository contains the example code for the
[Building Machines in Code](https://www.coderancher.us/series/building-machines-in-code/)
article series. Each directory is a checkpoint in the series, so learners can follow the
machine as it develops instead of encountering only the finished result.

## What you will learn

- How a fetch-decode-execute cycle works
- How registers, flags, memory, and buses cooperate
- How machine instructions are encoded and executed
- How a small assembler resolves labels and emits machine code
- How loaders, memory-mapped I/O, and disassemblers fit into an emulator toolchain

The code favors clarity and experimentation over performance. It is intended for learning,
not for production machine control or security-sensitive workloads.

## Learning path

| Part | Topic | Code |
| --- | --- | --- |
| [1](part-1/readme.txt) | Series introduction | Article only |
| [2](part-2/readme.txt) | Emulator and simulator foundations | Article only |
| [3](part-3/) | First Tiny-P CPU | `cpu.py` |
| [4](part-4/) | Tiny-P assembly exercises | CPU, assembly, and exercise scripts |
| [5](part-5/) | Building an assembler | Assembler and example program |
| [6](part-6/) | Loading machine code | CPU, loader, and example binary |
| [7](part-7/) | Connecting CPU, bus, and memory | Tiny-T system components |
| [8](part-8/) | Adding console I/O | Console-enabled Tiny-T system |
| [9](part-9/) | Completing the command-line toolchain | Assembler, loader, disassembler, and emulator |

Parts intentionally repeat code. That duplication preserves the state of the machine at each
article checkpoint and makes it easier to compare one lesson with the next.

## Requirements

- Python 3.10 or newer
- No third-party runtime dependencies
- `pytest` only when running the regression tests

Clone the repository:

```bash
git clone https://github.com/Monotoba/Building-Machines-In-Code.git
cd Building-Machines-In-Code
```

## Try the Part 9 toolchain

Assemble the included console-echo program:

```bash
python part-9/assembler.py \
  -i part-9/asm/echo.asm \
  -o echo.bin
```

Disassemble the resulting machine code:

```bash
python part-9/disassembler.py \
  -i echo.bin \
  -o echo.disasm
```

Run the interactive Tiny-T example:

```bash
cd part-9
python main.py
```

The console example waits for keyboard input and echoes characters. Press `Ctrl+C` to stop it.

## Tests

The regression suite covers the completed Part 9 teaching example, including instruction
encoding, CPU shifts, relocated memory, and command-line file handling.

```bash
python -m pip install pytest
pytest -q
```

CI runs the suite and compiles every Python example on Python 3.10 through 3.13.

## Contributing

Corrections and teaching improvements are welcome. Please keep changes focused and preserve
the historical progression between parts. For behavioral changes to Part 9, add or update a
regression test and run `pytest -q` before opening a pull request.

Useful contributions include:

- Fixing unclear explanations or examples
- Adding focused tests for existing instruction behavior
- Improving portability without obscuring the underlying computer concepts
- Reporting discrepancies between an article and its corresponding checkpoint

## Attribution and license

Building Machines in Code was created by Randall Morgan. If this material helps your own
project or teaching, attribution and a link to the
[article series](https://www.coderancher.us/series/building-machines-in-code/) are appreciated.

The code is available under the [BSD 2-Clause License](LICENSE), which requires preservation
of its copyright notice and license terms in source and binary redistributions.
