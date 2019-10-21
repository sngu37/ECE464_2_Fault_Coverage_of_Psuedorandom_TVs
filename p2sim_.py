import os
from numpy import binary_repr
from math import ceil
import Fault_simulator

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION:
def full_flist_generator(cktFile):
    netFile = open(cktFile, "r")
    # temporary empty list to be filled
    fault = []

    # Reading in the netlist file line by line
    for line in netFile:

        # NOT Reading any empty lines
        if (line == "\n"):
            continue
        # Removing spaces and newlines
        line = line.replace(" ", "")
        line = line.replace("\n", "")
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
        gate_output = lineSpliced[0]
        fault.append(gate_output)  # adding the gate output to the fault array

        # Read gate input wire and add to the fault array
        lineSpliced = lineSpliced[1].split("(")  # selecting the part in the brackets
        lineSpliced[1] = lineSpliced[1].replace(")", "")
        gate_inputs = lineSpliced[1].split(",")  # saving all the inputs of the current gate

        for inp in gate_inputs:
            terms = gate_output + "-IN-" + inp  # adding each input line of the current gate to the fault array,
            fault.append(terms)  # in the format "out-IN-in"


    Flist = open("full_fault_list.txt","w")

    # Initialize an empty full fault list to be filled
    full_fault_list = []

    # Consider each fault location both SA-1 and SA-0 and add this 2 faults to the full fault list
    for f in fault:
        fault_0 = f + "-SA-0"
        full_fault_list.append(fault_0)
        fault_1 = f + "-SA-1"
        full_fault_list.append(fault_1)

    # sorting the elements in the full fault list
    full_fault_list.sort()

    Flist.write("# Full SSA fault list\n\n")
    Flist.write("\n".join(full_fault_list))
    Flist.write("\n\n# total faults: {0}".format(len(full_fault_list)))
    Flist.close
    netFile.close

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION:
def TV_set_gen(cktFile):
    netFile = open(cktFile, "r")
    # count the number of inputs in the benchmark
    bit = 0
    for line in netFile:
        if (line[0:5] == "INPUT"):
            bit += 1
        if (line[0:5] == "OUTPUT"):
            break

    # Get desired seed from user
    while True:
        print("\n Choose a seed in [1,255]: ")
        seed = input()
        # seed = "42"
        s0 = int(seed)
        if (s0 < 1) or (s0 > 255):
            print("Incorrect seed. \n")
        else:
            break

    # open the 5 output files
    TV_A = open("TV_A.txt", "w")
    TV_B = open("TV_B.txt", "w")
    TV_C = open("TV_C.txt", "w")
    TV_D = open("TV_D.txt", "w")
    TV_E = open("TV_E.txt", "w")

    # define number of wanted TVs in each set:
    n = 255

    # generating TV set A
    for i in range(n):
        TV_A.write("{0}\n".format(binary_repr(s0 + i, bit)))

    # generating TV set B
    n_ceil = ceil(bit/8)
    rest = bit % 8
    for j in range(n):

        if (s0 + j) > 255:
            nom=binary_repr(s0 + j - 255, 8)
        else:
            nom=binary_repr(s0 + j, 8)

        tv = str(nom) * n_ceil
        if rest != 0:
            tv = tv[len(tv)-bit:len(tv)]
        TV_B.write("{0}\n".format(tv))

    # generating TV set C
    for j in range(n):
        tv=""
        for i in range(n_ceil):
            k = n_ceil - i -1
            if (s0 + j + k) > 255:
                nom=binary_repr(s0 + j + k - 255, 8)
            else:
                nom=binary_repr(s0 + j + k, 8)
            tv = tv + nom
        if rest != 0:
            tv = tv[len(tv)-bit:len(tv)]
        TV_C.write("{0}\n".format(tv))

    nom = binary_repr(46, 8)
    print("Done. TV sets generated")
    return


# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Main Function
def f_coverage(cktFile):


    # Select fault list file from user input
    while True:
        print("\n Read fault list file.")
        print("Enter your file name or press ENTER to use full fault list:")
        userInput = input()
        if userInput == "":
            full_list = True
            break
        else:
            fltFile = os.path.join(script_dir, userInput)
            if not os.path.isfile(faultFile):
                print("File does not exist. \n")
            else:
                break

    if full_list:
        full_flist_generator(cktFile)
        fltFile = "full_fault_list.txt"

    # Get desired batch size from user
    while True:
        print("\n Choose a batch size in [1,10]: ")
        batch = input()
        batch = round(int(batch))
        if (batch < 1) or (batch > 10):
            print("Incorrect batch size. Select an integer between 1 and 10. \n")
        else:
            break

    circuit = Fault_simulator.netRead(cktFile)

    # open the 5 TV set files
    TV_A = open("TV_A.txt", "r")
    TV_B = open("TV_B.txt", "r")
    TV_C = open("TV_C.txt", "r")
    TV_D = open("TV_D.txt", "r")
    TV_E = open("TV_E.txt", "r")

    outFile = open("f_cvg.csv", "w")
    outFile.write("batch# , TV_A , TV_B , TV_C , TV_D , TV_E, seed={0} , batch size={1}".format(10000,batch))

    TV_sets = [TV_A,TV_B,TV_C,TV_D,TV_E]
    coverage = {}
    for i in range(25):
        coverage[i] = [0,0,0,0,0]
    set_no = 0
    for set in TV_sets:
        print("---------------------->Analyzing TV_{0}".format(set_no+1))
        detection_list = []
        for i in range(25):
            print("--------->Analyzing batch# {0}".format(i+1))
            tv_list = []
            for j in range(batch):
                line = set.readline()
                tv_list.append(line)
            value , detection_list = Fault_simulator.f_sim(circuit, fltFile, tv_list , detection_list)
            coverage[i][set_no] = value
        print(coverage[g][set_no] for g in range(25))
        set_no += 1

    for i in range(25):
        outFile.write("\n{0} , {1} , {2} , {3} , {4} , {5}". format(i+1,coverage[i][0],coverage[i][1],coverage[i][2],coverage[i][3],coverage[i][4]))


    return
# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Main Function
def main():

    # Used for file access
    script_dir = os.path.dirname(__file__)

    # Select option for TV generation or fault coverage simulation (user's choice)
    while True:
        print("\n Choose what you’d like to do (1 or 2)")
        print("1: Test Vector Generation")
        print("2: Fault Coverage Simulation")
        opt = input()
        if (opt != "1") and (opt != "2"):
            print("Select a valid option: 1 or 2. \n")
        else:
            break


    # Select circuit benchmark file from user input
    while True:
        print("\n Read circuit benchmark file:")
        userInput = input()
        cktFile = os.path.join(script_dir, userInput)
        if not os.path.isfile(cktFile):
            print("File does not exist. \n")
        else:
            break

    if opt == "1":
        TV_set_gen(cktFile)

    if opt == "2":
        f_coverage(cktFile)


if __name__ == "__main__":
    main()