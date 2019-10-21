import os
from numpy import binary_repr
from math import ceil

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Main Function
def TV_set_gen(netFile):
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
    for i in range(n-1):
        TV_A.write("{0}\n".format(binary_repr(s0 + i, bit)))

    # generating TV set B
    n_ceil = ceil(bit/8)
    rest = bit % 8
    for j in range(n):
        tv = ""

        if (s0 + j) > 255:
            nom=binary_repr(s0 + j - 255, 8)

        else:
            nom=binary_repr(s0 + j, 8)

        tv = str(nom) * n_ceil
        if rest != 0:
            tv = tv[len(tv)-bit:len(tv)]
        TV_B.write("{0}\n".format(tv))


    return


# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Main Function
def f_coverage():




   return
# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Main Function
def main():

    # Used for file access
    script_dir = os.path.dirname(__file__)

    # Select option for TV generation or fault coverage simulation (user's choice)
    while True:
        print("\n Choose what you’d like to do (1, 2)")
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

    netFile = open(cktFile, "r")

    if opt == "1":
        TV_set_gen(netFile)

    if opt == "2":
        f_coverage()




if __name__ == "__main__":
    main()