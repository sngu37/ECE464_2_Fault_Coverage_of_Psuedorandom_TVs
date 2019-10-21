from __future__ import print_function
import os

# Function List:
# 1. wireRead: reads the benchmark file and individuates all the fault locations
# 2. main: The main function

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: wireRead
def wireRead(netName):

    # Opening the netlist file:
    netFile = open(netName, "r")

    #temporary empty list to be filled
    fault=[]

    # Reading in the netlist file line by line
    for line in netFile:

        # NOT Reading any empty lines
        if (line == "\n"):
            continue
        # Removing spaces and newlines
        line = line.replace(" ","")
        line = line.replace("\n","")
        # NOT Reading any comments
        if (line[0] == "#"):
            continue

        # Read a INPUT wire and add it to fault array: every input is a possible fault location
        if (line[0:5] == "INPUT"):
            # Removing everything but the line variable name
            line = line.replace("INPUT", "")
            line = line.replace("(", "")
            line = line.replace(")", "")

            # Appending to the fault array
            fault.append(line)

            continue

        # Skip the outputs, they are later considered as gate outputs
        if line[0:6] == "OUTPUT":
            continue

        # Read gate output wires, and add to the fault array
        lineSpliced = line.split("=")  # splicing the line at the equals sign to get the gate output wire
        gate_output=lineSpliced[0]
        fault.append(gate_output)    # adding the gate output to the fault array

        # Read gate input wire and add to the fault array
        lineSpliced = lineSpliced[1].split("(")            # selecting the part in the brackets
        lineSpliced[1] = lineSpliced[1].replace(")", "")
        gate_inputs=lineSpliced[1].split(",")         # saving all the inputs of the current gate

        for inp in gate_inputs:
            terms = gate_output + "-IN-" + inp         # adding each input line of the current gate to the fault array,
            fault.append(terms)                        # in the format "out-IN-in"

    print("All the possible fault locations: ")
    print(fault)
    return fault

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Main Function
def main():

    # Used for file access
    script_dir = os.path.dirname(__file__)  # absolute dir the script is in

    print("Full fault list generator: ")

    # Select circuit benchmark file
    while True:
        print("\n Read circuit benchmark file:")
        userInput = input()
        cktFile = os.path.join(script_dir, userInput)
        if not os.path.isfile(cktFile):
            print("File does not exist. \n")
        else:
            break

    print("\n Reading " + cktFile + " ... \n")

    # Getting the list of fault locations
    fault_location = wireRead(cktFile)

    # Select output file
    while True:
        print("\n Write full fault list output file: ")
        userInput = input()
        outputName = os.path.join(script_dir, userInput)
        if userInput == "":
            print("Enter a non empty file name. \n")
        else:
            break

    outputFile = open(outputName, "w")

    # Initialize an empty full fault list to be filled
    full_fault_list = []

    # Consider each fault location both SA-1 and SA-0 and add this 2 faults to the full fault list
    for fault in fault_location:
        fault_0 = fault + "-SA-0"
        full_fault_list.append(fault_0)
        fault_1 = fault + "-SA-1"
        full_fault_list.append(fault_1)

    # sorting the elements in the full fault list
    full_fault_list.sort()

    outputFile.write("# " + cktFile)
    outputFile.write("\n# Full SSA fault list\n\n")
    outputFile.write("\n".join(full_fault_list))
    outputFile.write("\n\n# total faults: {0}".format(len(full_fault_list)))
    print(full_fault_list)
    print("\n\n# total faults: {0}".format(len(full_fault_list)))
    outputFile.close


if __name__ == "__main__":
    main()