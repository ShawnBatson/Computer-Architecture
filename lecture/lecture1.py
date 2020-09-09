import sys

# PROGRAM COUNTER = pc.. built into computer. used to increment count
# operation coes
# OP Codes
PRINT_HELLO_WORLD = 1  # 0b00000001 binary
HALT = 2  # 0b00000010 binary
PRINT_NUM = 3  # 0b00000011 binary
SAVE_REG = 4  # OB00000100
PRINT_REG = 5
ADD = 6


# memory = [
#     PRINT_HELLO_WORLD,  # instruction
#     SAVE_REG,  # instruction
#     123,  # not an instruction, this is input. be mindful of memory position
#     1,  # register 1
#     PRINT_REG,  # 5
#     1,  # register 1
#     HALT  # 2
# ]  # memory is simply an array

memory = [0] * 256

running = True

registers = [0] * 8

pc = 0

# open a file and load into memory

#### LECTURE 2#####

# get file name from command line arguments
print(sys.argv)

if len(sys.argv) != 2:
    print("Usage: example_cpu.py filename")
    sys.exit(1)  # 0 error means good, 1 error means crash


def load_memory(filename):
    # open file and load into mem
    address = 0

    try:
        with open(sys.argv[1]) as f:  # open file
            for line in f:
                # break up lines on char that creates a comment
                split_line = line.split('#')  # split at the comment marker
                print(split_line)  # check the split

                # Removes whitespace and \n char
                # take the split line at 0, where the code should be and strip it
                code_value = split_line[0].strip()
                # Make sure that the value before the # symbol is not empty
                if split_line[0] == '':
                    continue

                num = int(code_value)
                memory[address] = num
                address += 1

    except FileNotFoundError:
        print(f"{sys.argv[1]} file not found")
        sys.exit(2)


load_memory(sys.argv[1])
while running:
    # read line by line from memory
    instruction = memory[pc]

    if instruction == PRINT_HELLO_WORLD:
        # print hello world,
        # move the pc up one to next instruction
        print('Hello World')
        pc += 1

    elif instruction == PRINT_NUM:
        # print the number in the next memory slot
        num = memory[pc + 1]
        print(num)
        pc += 2  # move the pointer 2 out, since we're using memory +1 for input material

    elif instruction == SAVE_REG:
        # save some value to some register
        # first number after instruction will be the value to store
        # second number after instrutcion will be register
        num = memory[pc + 1]
        reg_loc = memory[pc + 2]
        registers[reg_loc] = num
        pc += 3  # move 3 slots.

    elif instruction == PRINT_REG:
        reg_loc = memory[pc+1]
        print(registers[reg_loc])
        pc += 2

    elif instruction == ADD:
        reg_1 = memory[pc + 1]
        reg_2 = memory[pc + 2]
        registers[reg_1] += registers[reg_2]
        pc += 3
        # ADD takes TWO registers, adds their values,
        # and stores the result in the first register given
        # GET register 1
        # get register 2
        # add values to gether
        # store in register 1

    elif instruction == HALT:
        running = False
        pc += 1

    else:
        print(f'Unknown instruction {instruction}')
        sys.exit(1)  # this says the program exits not cleanly/crashed
