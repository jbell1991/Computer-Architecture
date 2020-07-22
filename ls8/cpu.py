"""CPU functionality."""

import sys

# instruction codes
HLT = 0b00000001 
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101 
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # hold 256 bytes of memory
        self.ram = [0] * 256
        # hold 8 general-purpose registers
        self.reg = [0] * 8
        # program counter
        self.pc = 0
        # stack pointer
        self.sp = 7
        self.running = True
    
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, filename=None):
        """Load a program into memory."""

        address = 0

        with open(filename, 'r') as f:
            for line in f:
                line = line.split("#")
                line = line[0].strip()
                if line == '':
                    continue
                self.ram[address] = int(line, 2)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            # self.trace()
            # instruction register
            instruction_register = self.ram_read(self.pc)
            # in case the instructions need them
            operand_a, operand_b = self.ram_read(self.pc + 1), self.ram_read(self.pc + 2)
            # perform the actions needed for instruction per the LS-8 spec
            # halt the CPU (and exit the emulator)
            if instruction_register == HLT:
                self.running = False
            # set the value of the register to an integer
            elif instruction_register == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            # print numeric value stored in the given register
            elif instruction_register == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif instruction_register == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif instruction_register == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            elif instruction_register == PUSH:
                # decrement the stack pointer
                self.reg[self.sp] -= 1
                self.ram_write(self.reg[operand_a], self.reg[self.sp])
                self.pc += 2
            elif instruction_register == POP:
                self.reg[operand_a] = self.ram_read(self.reg[self.sp])
                # increment the stack pointer
                self.reg[self.sp] += 1
                self.pc += 2
            elif instruction_register == CALL:
                self.reg[self.sp] -= 1
                self.ram_write(self.pc + 2, self.reg[self.sp])
                self.pc = self.reg[operand_a]
            elif instruction_register == RET:
                self.pc = self.ram_read(self.reg[self.sp])
                self.reg[self.sp] += 1
            else: 
                print("Instruction not valid")
