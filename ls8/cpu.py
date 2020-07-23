"""CPU functionality."""

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

        self.branch = {
            HLT: self.hlt,
            LDI: self.ldi,
            PRN: self.prn,
            POP: self.pop,
            PUSH: self.push,
            CALL: self.call,
            RET: self.ret,
            ADD: self.add,
            SUB: self.sub,
            MUL: self.mul,
            DIV: self.div,
            MOD: self.mod,
                       }

        self.reg = bytearray(8)
        self.ram = bytearray(256)
        self.reg[SP] = 0xF4

        # internal registers
        self.PC = 0
        self.IR = 0

        self.MAR = 0
        self.MDR = 0
        
        self.FL = 0

    def hlt(self, reg_num, value):
        sys.exit()

    def ldi(self, reg_num, value):
        self.reg[reg_num] = value

    def prn(self, reg_num):
        print(self.reg[reg_num])

    # stack
    def pop(self, reg_num):
        self.reg[reg_num] = self.ram_read(self.reg[SP])
        self.reg[SP] += 1

    def push(self, reg_num):
        self.reg[SP] -= 1
        self.ram_write(self.reg[reg_num], self.reg[SP])

    # sub
    def call(self, reg_num):
        self.ldi(4, self.PC + 2)
        self.push(4)
        self.PC = self.reg[reg_num]

    def ret(self):
        self.pop(4)
        self.PC = self.reg[4]

    # arithmetic ops
    def add(self, reg_a, reg_b):
        self.alu("ADD", reg_a, reg_b)

    def sub(self, reg_a, reg_b):
        self.alu("SUB", reg_a, reg_b)

    def mul(self, reg_a, reg_b):
        self.alu("MUL", reg_a, reg_b)
    
    def div(self, reg_a, reg_b):
        self.alu("DIV", reg_a, reg_b)

    def mod(self, reg_a, reg_b):
        self.alu("MOD", reg_a, reg_b)

    # memory
    def ram_read(self, address):
        # print(f'RAM at {self.PC} has the address value {self.ram[address]}. ')
        return self.ram[address]

    def ram_write(self, value, address):
        # print(f'Value {self.ram[address]} was written to RAM at {self.PC} address {self.ram[address]}. ')
        self.ram[address] = value

    def load(self):
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

        # completely move load to cpu.py
        if len(sys.argv) != 2:
            print("Usage: ls8.py <filename>")
            sys.exit()

        with open(sys.argv[1]) as file:
            program = [int(line[:line.find('#')].strip(), 2)
                       for line in file
                       if line != '\n' and line[0] != '#']

        for instruction in program:
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
            self.PC,
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
        self.IR = self.ram_read(self.PC)
        op_a = self.ram_read(self.PC + 1)
        op_b = self.ram_read(self.PC + 2)

        # while cpu is running
        while self.IR != HLT:
            nums = (self.IR & 0b11000000) >> 6
            pc_set = (self.IR & 0b00010000) >> 4
            try:
                if nums == 0:
                    self.branch[self.IR]()
                elif nums == 1:
                    self.branch[self.IR](op_a)
                else:
                    self.branch[self.IR](op_a, op_b)

            except KeyError:
                raise Exception("Unsupported operation {self.IR} at address {self.PC}.")

            if pc_set == 0:
                self.PC += nums + 1

            self.IR = self.ram_read(self.PC)
            op_a = self.ram_read(self.PC + 1)
            op_b = self.ram_read(self.PC + 2)