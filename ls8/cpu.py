"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.running = False
        self.SP = 7
        self.reg[self.SP] = 0xf4
        self.FL = 0
        self.branchtable = {}
        self.branchtable[0b10000010] = self.handleLDI
        self.branchtable[0b01000111] = self.handlePRN
        self.branchtable[0b10100010] = self.handleMUL
        self.branchtable[0b00000001] = self.handleHLT
        self.branchtable[0b01000110] = self.handlePOP
        self.branchtable[0b01000101] = self.handlePUSH
        self.branchtable[0b01010000] = self.handleCALL
        self.branchtable[0b00010001] = self.handleRET
        self.branchtable[0b10100000] = self.handleADD
        self.branchtable[0b10100111] = self.handleCMP
        self.branchtable[0b01010100] = self.handleJMP
        self.branchtable[0b01010101] = self.handleJEQ
        self.branchtable[0b01010110] = self.handleJNE
        # Add the ALU operations: `AND` `OR` `XOR` `NOT` `SHL` `SHR` `MOD`
        self.branchtable[0b10101000] = self.handleAND
        self.branchtable[0b10101010] = self.handleOR
        self.branchtable[0b10101011] = self.handleXOR
        self.branchtable[0b01101001] = self.handleNOT
        self.branchtable[0b10101100] = self.handleSHL
        self.branchtable[0b10101101] = self.handleSHR
        self.branchtable[0b10100100] = self.handleMOD

    def handleLDI(self):  # load instructions with ops above
        opA = self.ram_read(self.pc + 1)
        opB = self.ram_read(self.pc + 2)
        self.reg[opA] = opB
        self.pc += 3  # this uses 3 movements

    def handlePRN(self):
        opA = self.ram_read(self.pc + 1)
        x = self.reg[opA]  # set the value to the printing value
        print(x)  # print the value
        self.pc += 2  # this takes two movements

    def handleMUL(self):
        opA = self.ram_read(self.pc + 1)
        opB = self.ram_read(self.pc + 2)
        self.alu('MUL', opA, opB)
        self.pc += 3

    def handleHLT(self):
        self.running = False  # set running to false
        # self.pc += 1  # this takes one movement.

    def handlePOP(self):
        given_register = self.ram[self.pc + 1]  # set the register
        reg_address = self.reg[self.SP]  # set the register address
        value_from_memory = self.ram[reg_address]  # set the value
        self.reg[given_register] = value_from_memory
        self.reg[self.SP] += 1  # move the SP
        self.pc += 2  # move the PC

    def handlePUSH(self):
        self.reg[self.SP] -= 1  # move the SP
        given_register = self.ram[self.pc + 1]  # set the register
        value_in_memory = self.reg[given_register]  # set the value
        memory_address = self.reg[self.SP]  # set the memory address
        self.ram[memory_address] = value_in_memory  # align
        self.pc += 2  # move the PC

    def handleCALL(self):
        given_register = self.ram[self.pc + 1]  # set the register
        self.reg[self.SP] -= 1  # move the sp
        r = self.pc + 2  # save the spot
        self.ram[self.reg[self.SP]] = r  # point to the return
        # set the go_to variable for the subroutine
        go_to = self.reg[given_register]
        self.pc = go_to  # move the pc to the go_to

    def handleRET(self):
        r = self.ram[self.reg[self.SP]]  # return to -
        self.reg[self.SP] += 1  # move the SP one
        self.pc = r  # move the pc

    def handleADD(self):
        opA = self.ram_read(self.pc + 1)
        opB = self.ram_read(self.pc + 2)
        self.alu('ADD', opA, opB)
        self.pc += 3

    def handleCMP(self):
        opA = self.ram_read(self.pc + 1)  # set opA
        opB = self.ram_read(self.pc + 2)  # set opB
        self.alu('CMP', opA, opB)  # set the ALU
        self.pc += 3  # move the pc

    def handleJMP(self):
        opA = self.ram_read(self.pc + 1)  # set the operand
        self.pc = self.reg[opA]  # set the pc to the operand chosen

    def handleJEQ(self):
        opA = self.ram_read(self.pc + 1)
        if self.fl == 1:
            self.pc = self.reg[opA]
        else:
            self.pc += 2

    def handleJNE(self):
        opA = self.ram_read(self.pc + 1)
        if self.fl != 1:
            self.pc = self.reg[opA]
        else:
            self.pc += 2
# Add the ALU operations: `AND` `OR` `XOR` `NOT` `SHL` `SHR` `MOD`

    def handleAND(self):
        opA = self.ram_read(self.pc + 1)  # set opA
        opB = self.ram_read(self.pc + 2)  # set opB
        # throw into ALU
        result = self.alu("AND", self.reg[opA], self.reg[opB])
        self.reg[opA] = result  # set the result to opA for the "and"
        self.pc += 3

    def handleOR(self):
        opA = self.ram_read(self.pc + 1)  # set opA
        opB = self.ram_read(self.pc + 2)  # set opB
        result = self.alu("OR", self.reg[opA], self.reg[opB])
        self.reg[opA] = result
        self.pc += 3

    def handleXOR(self):
        opA = self.ram_read(self.pc + 1)  # set opA
        opB = self.ram_read(self.pc + 2)  # set opB
        result = self.alu("XOR", self.reg[opA], self.reg[opB])
        self.reg[opA] = result
        self.pc += 3

    def handleNOT(self):
        opA = self.ram_read(self.pc + 1)  # set opA
        opB = self.ram_read(self.pc + 2)  # set opB
        result = self.alu("NOT", self.reg[opA], self.reg[opB])
        self.reg[opA] = result
        self.pc += 2

    def handleSHL(self):
        opA = self.ram_read(self.pc + 1)  # set opA
        opB = self.ram_read(self.pc + 2)  # set opB
        result = self.alu("SHL", self.reg[opA], self.reg[opB])
        self.reg[opA] = result
        self.pc += 3

    def handleSHR(self):
        opA = self.ram_read(self.pc + 1)  # set opA
        opB = self.ram_read(self.pc + 2)  # set opB
        result = self.alu("SHR", self.reg[opA], self.reg[opB])
        self.reg[opA] = result
        self.pc += 3

    def handleMOD(self):
        opA = self.ram_read(self.pc + 1)  # set opA
        opB = self.ram_read(self.pc + 2)  # set opB
        if self.reg[opB] == 0:
            print("You cannot divide by 0")
            self.handleHLT()
        else:
            result = self.alu("MOD", self.reg[opA], self.reg[opB])
            self.reg[opA] = result
            self.pc += 3

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""
        address = 0
        if len(sys.argv) != 2:
            print("Usage: example_cpu.py filename")
            sys.exit(1)

        try:
            with open(f'examples/{sys.argv[1]}') as f:
                for line in f:
                    split_line = line.split('#')
                    code_value = split_line[0].strip()
                    if code_value == '':
                        continue
                    if code_value == "#":
                        continue
                    num = code_value
                    self.ram[address] = int(num, 2)  # ER
                    address += 1
        except FileNotFoundError:
            print(f'{sys.argv[1]} file not found')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'CMP':
            if self.reg[reg_a] < self.reg[reg_b]:  # if reg a less reg b,
                self.fl = 0b00000100  # set fl to L
            elif self.reg[reg_a] > self.reg[reg_b]:  # if reg a greater reg b
                self.fl = 0b00000010  # set fl to G
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001  # set fl to E
        # Add the ALU operations: `AND` `OR` `XOR` `NOT`
        elif op == "AND":
            return reg_a & reg_b
        elif op == "OR":
            return reg_a | reg_b
        elif op == "XOR":
            return reg_a ^ reg_b
        elif op == "NOT":
            return ~reg_a
        elif op == "SHL":
            return reg_a << reg_b
        elif op == "SHR":
            return reg_a >> reg_b
        elif op == "MOD":
            return int(reg_a) % int(reg_b)
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
        self.running = True

        while self.running == True:

            IR = self.ram[self.pc]
            if IR in self.branchtable:
                do = self.branchtable[IR]
                do()
            else:
                self.running = False
