
import re, argparse, os

def spellCheck(inp, spelling):
    inp = inp.split()
    capitals = checkCapitals(inp)
    punctuation = checkPunctuation(inp)
    numbers = checkNumbers(inp)

    words = [re.sub("[^a-z]","",w.lower()) for w in inp]
    words = list(filter(lambda item: item!="",words))

    spelling = spelling.split()
    numWords = len(words)
    correct = 0
    incorrect = 0
    for word in words:
        if word in spelling:
            correct +=1
        else:
            incorrect += 1

    out  = "u49728rt\n"
    out += "Formatting ###################\n"
    out += "Number of upper case letters changed: " + str(capitals) + "\n"
    out += "Number of punctuations removed: " + str(punctuation) + "\n"
    out += "Number of numbers removed: " + str(numbers) + "\n"
    out += "Spellchecking ###################\n"
    out += "Number of words: " + str(numWords) + "\n"
    out += "Number of correct words: " + str(correct) + "\n"
    out += "Number of incorrect words: " + str(incorrect)

    return out

def checkCapitals(words):
    total = 0
    for word in words:
        total += len(re.findall("[A-Z]",word))
    return total

def checkPunctuation(words):
    total = 0
    for word in words:
        total += len(re.findall("[\.\?\!\,\:\;\-\(\)\[\]\{\}\'\"\#\@\~\>\<\*\&\%\$\£\=\+\-\/]",word))
        elipsis = True
        while elipsis:
            elipsis = False
            if len(re.findall("[.]",word)) > 2:
                listWord = list(word)
                first = listWord.index(".")
                if first < len(listWord)-2:
                    elipsis = True
                    if listWord[first+1] == "." and listWord[first+2] == ".":
                        total -= 2
                        first += 2
                    word = word[first::]

    return total

def checkNumbers(words):
    total = 0
    for word in words:
        total += len(re.findall("[0-9]",word))
    return total







parser = argparse.ArgumentParser()
parser.add_argument("wordFile", metavar="path", help="Path to English words")
parser.add_argument("inFolder", metavar="path", help="Path to input Folder")
parser.add_argument("outFolder", metavar="path", help="Path to output folder")
args = parser.parse_args()


fileNames = os.listdir(str(args.inFolder))
filePaths = [os.path.join(args.inFolder,fileName) for fileName in fileNames]
spellings = open(args.wordFile).read()

for pathIndex in range(len(filePaths)):
    out = spellCheck(open(filePaths[pathIndex]).read(),spellings)
    outFileName = fileNames[pathIndex].split(".")
    outFileName = outFileName[0] + "_u49728rt.txt"
    try:
        f = open(os.path.join(args.outFolder, outFileName), "w")
    except:
        f = open(os.path.join(args.outFolder, outFileName), "x")
    f.write(out)