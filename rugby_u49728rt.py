import argparse, os

def rugby(input):
    input = input.split("T")
    vals = {"t":5,"c":2,"p":3,"d":3}
    t1 = 0
    t2 = 0
    del input[0]
    for i in input:
        if i[0] == "1":
            t1 += vals[i[1]]
        else:
            t2 += vals[i[1]]
    return [t1,t2]

parser = argparse.ArgumentParser()
parser.add_argument("inFolder", metavar="path", help="Path to input Folder")
parser.add_argument("outFolder", metavar="path", help="Path to output folder")
args = parser.parse_args()


fileNames = os.listdir(str(args.inFolder))
filePaths = [os.path.join(args.inFolder,fileName) for fileName in fileNames]

for pathIndex in range(len(filePaths)):
    out = rugby(open(filePaths[pathIndex]).read())
    outFileName = fileNames[pathIndex].split(".")
    outFileName = outFileName[0] + "_u49728rt.txt"
    f = open(os.path.join(args.outFolder, outFileName), "x")
    f.write(str(out[0])+":"+str(out[1]))

