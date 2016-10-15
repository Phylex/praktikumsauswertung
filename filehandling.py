import os
import sys

def verboseCheckfile(filepath="")
    while(!(os.path.exists(filepath)) && !(filepath=="exit")):
        print ("This File does not Exist!")
        filepath = input ("Enter the Filepath\(relative or absolute\):")
    if filepath == exit:
        return 0
    else:
        return 1

if( __name__ == "__main__"):
    filepath="./realfile"
    print(verboseCheckfile(filepath))
    print(verboseCheckfile(filepath))
