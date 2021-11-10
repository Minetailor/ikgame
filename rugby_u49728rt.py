import argparse

def rugby(input):
    input = input.split("T")
    vals = {"t":5,"c":2,"p":3,"d":3}
    t1 = 0
    t2 = 0
    del input[0]
    for i in input:
        print(i)
        if i[0] == "1":
            t1 += vals[i[1]]
        else:
            t2 += vals[i[1]]
    return [t1,t2]

parser = argparse.ArgumentParser()
parser.add_argument("inFile", metavar="path", type=str, help="Path to input file")
parser.add_argument("outFile", metavar="path", type=str, help="Path to output file")
args = parser.parse_args()

out = rugby(open(args.inFile).read())
f = open(args.outFile, "w")
f.write(str(out[0])+":"+str(out[1]))
