"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.program_count = 0
        self.commands = {
            0b00000001: self.hlt,
            0b10000010: self.ldi,
            0b01000111: self.prn
        }

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def hlt(self, op_a, op_b):
        return (0, False)

    def ldi(self, op_a, op_b):
        self.reg[op_a] = op_b
        return (3, True)

    def prn(self, op_a, op_b):
        print(self.reg[op_a])
        return (2, True)

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
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
            self.program_count,
            #self.fl,
            #self.ie,
            self.ram_read(self.program_count),
            self.ram_read(self.program_count + 1),
            self.ram_read(self.program_count + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            instruction_register = self.ram_read(self.program_count)
            op_a = self.ram_read(self.program_count + 1)
            op_b = self.ram_read(self.program_count + 2)

            try:
                f = self.commands[instruction_register]
                operation_op = f(op_a, op_b)
                running = operation_op[1]
                self.program_count += operation_op[0]
            except:
                print(f"Error: Instruction {instruction_register} not found")
                sys.exit(1)
        
