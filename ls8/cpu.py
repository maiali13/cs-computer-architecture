"""CPU functionality
"""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

MUL = 0b10100010
DIV = 0b10100011
ADD = 0b10100000
SUB = 0b10100001
MOD = 0b10100100

POP = 0b01000110
PUSH = 0b01000101

CALL = 0b01010000
RET = 0b00010001

# register num for stack pointer
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.PC = 0
        # self.bytes = 256
        # self.ram = [0] * self.bytes
        self.ram = bytearray(256)
        self.reg = bytearray(8)
        self.reg[SP] = 0xF4
        self.branch = {
            HLT: self.hlt,
            LDI: self.ldi,
            CALL: self.call,
            RET: self.ret,
            PRN: self.prn,
            POP: self.pop,
            PUSH: self.push,
            ADD: self.alu,
            SUB: self.alu,
            MUL: self.alu,
            DIV: self.alu,
            MOD: self.alu,
        }

    def hlt(self, op_a, op_b):
        sys.exit()

    def ldi(self, op_a, op_b):
        self.reg[op_a] = op_b

    def prn(self, op_a, op_b=None):
        print(self.reg[op_a])
    
    # stack
    def pop(self, reg_num):
        self.reg[reg_num] = self.ram_read(self.reg[SP])
        self.reg[SP] += 1

    def push(self, reg_num):
        self.reg[SP] -= 1
        self.ram_write(self.reg[reg_num], self.reg[SP])
    
    # subroutine
    def call(self, op_a, op_b=None):
        self.reg[SP] -= 1
        self.ram_write(self.reg[SP], self.PC + 2)
        self.PC = self.reg[op_a]

    def ret(self, op_a, op_b=None):
        self.PC = self.ram_read(self.reg[SP])
        self.reg[SP] += 1  

    def ram_read(self, address):
        """
        accepts the address to read and returns the value stored there
        """
        print(f'RAM at {self.PC} has the address value {self.ram[address]}. ')
        return self.ram[address]
    
    def ram_write(self, value, address):
        """
        accepts a value to write, and the address to write it to
        """
        print(f'Value {self.ram[address]} was written to RAM at {self.PC} address {self.ram[address]}. ')
        self.ram[address] = value
        
    def load(self, file):
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
        # add
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # subtract
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        # multiply
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        # divide
        elif op == "DIV":
            self.reg[reg_a] //= self.reg[reg_b]
        # modulo
        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]

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
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU.
        reads memory address and stores result in IR
        """
        running = True
        # update for branch table
        while running:
            self.IR = self.ram_read(self.PC)
            op_a = self.ram_read(self.PC + 1)
            op_b = self.ram_read(self.PC + 2)

            nums = ((self.IR & 0b11000000) >> 6)
            ALU_ops = ((self.IR & 0b11000000) >> 5)
            PC_set = ((self.IR & 0b11000000) >> 4)
            
            if self.IR in self.branch:
                if ALU_ops:
                    self.branch[self.IR](op_a, op_b)
                else:
                    self.branch[self.IR](op_a, op_b)
            else:
                raise Exception('Unsupported operation {self.IR} at address {self.PC}.')
            
            if not PC_set:
                self.PC += nums + 1 # opcode
            
