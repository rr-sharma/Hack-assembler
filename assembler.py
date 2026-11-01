
# PART 1: TABLES

# Predefined symbols
symbols = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576
}
for i in range(16):
    symbols["R" + str(i)] = i


# Computation table
comp = {
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",

    "M":   "1110000",
    "!M":  "1110001",
    "-M":  "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}


# Destination table
dest = {
    "":    "000",
    "M":   "001",
    "D":   "010",
    "MD":  "011",
    "A":   "100",
    "AM":  "101",
    "AD":  "110",
    "AMD": "111"
}


# Jump table
jump = {
    "":    "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}


# PART 2: READ THE ASSEMBLY FILE
input_file= input("enter the name of file to be converted :")
output_file =input("enter the name of the asm file :")

file = open(input_file, "r")
lines = file.readlines()
file.close()

# Remove comments and empty lines
clean_lines = []

for line in lines:
    line = line.split("//")[0].strip()

    if line != "":
        clean_lines.append(line)


# PART 3: FIRST PASS
# Find labels and store their ROM addresses.

rom_address = 0

for line in clean_lines:

    if line[0] == "(" and line[-1] == ")":
        label = line[1:-1]
        symbols[label] = rom_address

    else:
        rom_address = rom_address + 1


# PART 4: SECOND PASS
# Translate each instruction into binary.

machine_code = []
next_variable_address = 16

for line in clean_lines:

    # Labels are not machine instructions.
    if line[0] == "(" and line[-1] == ")":
        continue

    # A-instruction: @value
    if line[0] == "@":

        value = line[1:]

        # Is the value a number?
        if value.isdigit():
            address = int(value)

        else:
            # Is this a symbol we already know?
            if value in symbols:
                address = symbols[value]

            else:
                # A new variable starts at RAM address 16.
                address = next_variable_address
                symbols[value] = address
                next_variable_address = next_variable_address + 1

        binary = format(address, "016b")
        machine_code.append(binary)

    # C-instruction: dest=comp;jump
    else:

        destination = ""
        computation = line
        jump_command = ""

        # Separate the destination, if present.
        if "=" in computation:
            parts = computation.split("=")
            destination = parts[0]
            computation = parts[1]

        # Separate the jump command, if present.
        if ";" in computation:
            parts = computation.split(";")
            computation = parts[0]
            jump_command = parts[1]

        # Convert the three fields into binary.
        binary = (
            "111"
            + comp[computation]
            + dest[destination]
            + jump[jump_command]
        )

        machine_code.append(binary)


# PART 5: SAVE THE MACHINE CODE

file = open(output_file, "w")

for instruction in machine_code:
    file.write(instruction + "\n")

file.close()

print("Assembly completed!")
print("Instructions generated:", len(machine_code))
print("Output saved to:", output_file)
