"""Regression tests for the completed Tiny-T teaching example."""

import subprocess
import sys
from pathlib import Path

from assembler import Assembler, Lexer
from bus import Bus
from cpu import CPU
from disassembler import Disassembler
from memory import Memory


ROOT = Path(__file__).resolve().parents[1]
PART_9 = ROOT / "part-9"


def test_assembler_accepts_halt_without_operand():
    assert Assembler(Lexer(), "HLT").parse() == "0000 0\n"
    assert "HLT" in Disassembler.disasm("0000 0\n")


def test_shift_instructions_move_bits_in_named_direction():
    cpu = CPU(Bus())
    cpu.set_accumulator(0b0010)
    cpu.execute(0x9, 0)
    assert cpu.accumulator == 0b0100

    cpu.execute(0xA, 0)
    assert cpu.accumulator == 0b0010


def test_memory_range_is_half_open_and_respects_start_address():
    memory = Memory(4, 8)
    memory.set_location(0x100)

    assert memory.should_respond(0x100)
    assert memory.should_respond(0x103)
    assert not memory.should_respond(0x104)

    memory.write(0x100, 0x1FF)
    assert memory.read(0x100) == 0xFF


def test_command_line_output_option_and_default_paths(tmp_path):
    source_dir = tmp_path / "example.with.dots"
    source_dir.mkdir()
    source = source_dir / "echo.program.asm"
    source.write_text("ORG. 0x0000\nHLT\n", encoding="utf-8")
    explicit_binary = tmp_path / "explicit.bin"

    subprocess.run(
        [sys.executable, str(PART_9 / "assembler.py"), "-i", str(source), "-o", str(explicit_binary)],
        check=True,
    )
    assert explicit_binary.read_text(encoding="utf-8") == "0000 0\n"

    subprocess.run(
        [sys.executable, str(PART_9 / "assembler.py"), "-i", str(source)],
        check=True,
    )
    default_binary = source.with_suffix(".bin")
    assert default_binary.exists()

    subprocess.run(
        [sys.executable, str(PART_9 / "disassembler.py"), "-i", str(default_binary)],
        check=True,
    )
    assert "HLT" in default_binary.with_suffix(".disasm").read_text(encoding="utf-8")
