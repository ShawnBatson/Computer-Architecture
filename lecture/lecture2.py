# BITWISE
# BOOLEAN ALGEBRA.
# LOGIC GATE - physical piece of hardware that creates a truthtable

# a = 0b01011010
# b = 0b10101111
# # and
# print(bin(a & b))
# # or
# print(bin(a | b))
# # x-or
# print(bin(a ^ b))


########## BIT SHIFTING ###################

# shifting bits left or right.  << and >> for shifting a direction

# A >> 1   means shift A right one bit
# A << 3   means shift A left three bits

# 0b1110 >> 1     =    0b0111
# ob1110 << 3     =    0b 1110000

# # division,  shift by 1 is div by 2, shift by 2 is div by 4, shift by 3 is div by 8
# print(bin(0b1110 >> 1))

# # mult.  shift by 1 is mult by 2, shift by 2 is mult by 4, shift by 3 is mult by 8
# print(bin(0b1110 << 3))


### BIT MASKING ###

# combination of shifting and boolean algebra to return a value for binary.

instruction = 0b10011010  # want center 1's. shift, then remove

shifted = instruction >> 3
print(bin(shifted))

mask = 0b00000011  # create the mask that will get the two desired digits as a 1
print(bin(shifted & mask))
#==============#
# same as above,
instruction1 = 0b10011010
mask1 = 0b00011000 & instruction1
shifted1 = mask1 >> 3


print(bin(shifted1))


#=============#

# instruction = 0b10000010
# shifted = instruction >> 6

# print(bin(shifted))
