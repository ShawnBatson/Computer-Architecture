"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0,
        self.reg = [0] * 8,
        self.ram = [0] * 256
        self.running = True

# `PC`: Program Counter, address of the currently executing instruction
# `IR`: Instruction Register, contains a copy of the currently executing instruction
# `MAR`: Memory Address Register, holds the memory address we're reading or writing
# `MDR`: Memory Data Register, holds the value to write or the value just read
# `FL`: Flags, see below

    def ram_read(self, MAR):
        self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8   # THIS is the initial register number 0, load data
            0b00000000,  # this is the register number to load (0)
            0b00001000,  # this is the value to load (number 8)
            0b01000111,  # PRN R0 # this instruction is to print
            0b00000000,  # this is register 0, the value that above instruction prints
            0b00000001,  # HLT # this is the halt
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

# * `IR`: Instruction Register, contains a copy of the currently executing instruction

    def run(self):
        """Run the CPU."""
        while self.running:
            IR = str(self.ram_read(self.pc))

# Meanings of the bits in the first byte of each instruction: `AABCDDDD`

            # * `AA` Number of operands for this opcode, 0-2
            # * `B` 1 if this is an ALU operation
            # * `C` 1 if this instruction sets the PC
            # * `DDDD` Instruction identifier
            # break down the information above and set it to variables
            # `AA B C DDDD`

            opco = IR[:2]  # the op code is the first two or "AA"
            aluOp = IR[2:3]  # the alu operation is "b"
            movePc = IR[3:4]  # this is the amount to move the pc
            instructId = IR[4:]  # this is the instruction ID

            # binary 0b or 0B
            # print("For 1010, int is:", int('1010', 2))
            # print("For 0b1010, int is:", int('0b1010', 2))
            # THE ABOVE CODE IS A RESOURCE From PROGRAMMIZ.com

            if int(opco, 2) == 2:  # if there are two values (print, register, value)
                # label the first operand
                opA = int(self.ram_read(self.pc + 1), 2)
                # label the second operand
                opB = int(self.ram_read(self.pc + 1), 2)
            elif int(opco, 2) == 1:  # else if there is one value (print)
                opA = int(self.ram_read(self.pc + 1), 2)

            # this is the load
            if IR == '10000010':  # load instructions with ops above
                self.reg[opA] = opB
                self.pc += 3  # this uses 3 movements
            # this is the print
            elif IR == '01000111':
                x = self.reg[opA]  # set the value to the printing value
                print(x)  # print the value
                self.pc += 2  # this takes two movements
            elif IR == '00000001':  # halt
                self.running = False  # set running to false
                self.pc += 1  # this takes one movement.
