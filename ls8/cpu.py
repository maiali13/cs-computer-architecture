"""CPU functionality
"""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.PC = 0
        # self.bytes = 256
        # self.ram = [0] * self.bytes
        self.ram = bytearray(32)
        self.register = bytearray(8)

    def ram_read(self, address):
        """
        accepts the address to read and returns the value stored there
        """
        print(f'RAM at {self.pc} has the address value {self.ram[address]}. ')
        return self.ram[address]
    
    def ram_write(self, value, address):
        """
        accepts a value to write, and the address to write it to
        """
        print(f'Value {self.ram[address]} was written to RAM at {self.pc} address {self.ram[address]}. ')
        self.ram[address] = value
        
    def load(self, filename):
        """Load a program into memory."""
        address = 0

        # # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000, # 0
        #     0b00001000, # 8
        #     0b01000111, # PRN R0
        #     0b00000000, # 0
        #     0b00000001, # HLT

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        with open(file) as f:
            for line in f:
                # ignore comments
                line = line.split("#")
                try:
                    # convert to into to store in ram
                    instruction = int(line[0], 2)

                except ValueError:
                    continue

                self.ram[address] = instruction
                address += 1



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
        """Run the CPU.
        reads memory address and stores result in IR
        """
        self.IR = self.ram_read(self.PC)
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)

        while self.IR != HLT: # while cpu is running
            if self.IR == LDI: # set value of reg to an int
                self.register[operand_a] = operand_b
                self.PC += 3

            elif self.IR == PRN: # print value stored in the reg
                print(self.register[operand_a])
                self.PC += 2

            else:
                raise Exception('Unsupported operation {self.IR} at address {self.PC}.')
            
            self.IR = self.ram_read(self.PC)
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)
            
