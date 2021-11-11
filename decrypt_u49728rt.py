import argparse, os

def morseCode(text):
    morse = {   "/"     : " ",
                ".-"    : "a",
                "-..."  : "b",
                "-.-."  : "c",
                "-.."   : "d",
                "."     : "e",
                "..-."  : "f",
                "--."   : "g",
                "...."  : "h",
                ".."    : "i",
                ".---"  : "j",
                "-.-"   : "k",
                ".-.."  : "l",
                "--"    : "m",
                "-."    : "n",
                "---"   : "o",
                ".--."  : "p",
                "--.-"  : "q",
                ".-."   : "r",
                "..."   : "s",
                "-"     : "t",
                "..-"   : "u",
                "...-"  : "v",
                ".--"   : "w",
                "-..-"  : "x",
                "-.--"  : "y",
                "--.."  : "z",
                ".-.-.-": ".",
                "--..--": ",",
                "..--..": "?",
                "-..-." : "/",
                "...-.-": "@",
                "-.-.--": "!",
                "---..-": ":",
                "-....-": "-",
                "-.--.-": ")",
                "-.--." : "(",
                ".----.": "'",
                ".-..-.": '"',
                "-.-.-.": ";",
                ".----" : "1",
                "..---" : "2",
                "...--" : "3",
                "....-" : "4",
                "....." : "5",
                "-...." : "6",
                "--..." : "7",
                "---.." : "8",
                "----." : "9",
                "-----" : "0"}

    final = ""
    for letter in text.split():
        final += morse[letter]
    return final

def caesar(text):
    cText = "abcdefghijklmnopqrstuvwxyz"
    alphabet = []
    for letter in cText:
        alphabet.append(letter)
    final = ""
    for word in text.split():
        for letter in word:
            pos = alphabet.index(letter)
            cPos = pos - 3
            final += (alphabet[cPos])
        final += " "
    return final

def hexadecimal(text):
    text = text.split()
    final = ""
    for letter in text:
        final += chr(int(letter,16))
    return final

def decrypt(inp):
    inp = inp.split(":")
    cipher = inp[0]
    encrypted = inp[1]
    if cipher == "Morse Code":
        return morseCode(encrypted)
    elif cipher == "Caesar Cipher(+3)":
        return caesar(encrypted)
    elif cipher == "Hex":
        return hexadecimal(encrypted)


parser = argparse.ArgumentParser()
parser.add_argument("inFolder", metavar="path", help="Path to input Folder")
parser.add_argument("outFolder", metavar="path", help="Path to output folder")
args = parser.parse_args()


fileNames = os.listdir(str(args.inFolder))
filePaths = [os.path.join(args.inFolder,fileName) for fileName in fileNames]

for pathIndex in range(len(filePaths)):
    out = decrypt(open(filePaths[pathIndex]).read())
    outFileName = fileNames[pathIndex].split(".")
    outFileName = outFileName[0] + "_u49728rt.txt"
    try:
        f = open(os.path.join(args.outFolder, outFileName), "w")
    except:
        f = open(os.path.join(args.outFolder, outFileName), "x")
    f.write(str(out))