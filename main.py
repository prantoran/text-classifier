import os
import csv
import sys
import math
import argparse
import subprocess

class Label:
    Missing = ""
    No = "N"
    Yes = "Y"

def parseArgsnFlags():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interactive", 
        help="open prompt for querying model", action = "store_true")
    
    parser.add_argument("-l", "--labelcol", 
        help="column number of labels in the csv file", default = 3)
    
    parser.add_argument("-d", "--datacol", 
        help="column number of data in the csv file", default = 4)

    parser.add_argument("-f", "--filename",
        help="csv file name to use data source", default="")
    
    return parser.parse_args()


def process(srcFile, writeFormat,dstTrainFile, dstValidFile, labelCol, dataCol):

    if writeFormat != "a" and writeFormat != "w":
        print("output file write format not accepted")
        return False

    positives = []
    negatives = []
    
    with open(srcFile, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in filereader:
            # print("row:", row)
            label = row[labelCol]
            data = row[dataCol]
            if label == Label.Missing:
                continue
            if label == Label.Yes:
                positives.append("__label__relavant " + data + "\n")
            elif label == Label.No:
                negatives.append("__label__irrelevant " + data + "\n")

    plen = len(positives)
    nlen = len(negatives)

    mlen = min(plen, nlen)

    trainLen = math.floor(mlen / 5) * 4

    print("positive data:", plen," negative data:", nlen)


    with open(dstTrainFile, writeFormat, newline='\n') as outFile:
        for i in range(trainLen):
            outFile.write(positives[i])
            outFile.write(negatives[i])
        
        if plen > mlen:
            for i in range(mlen+1, plen):
                outFile.write(positives[i])
        
        if nlen > mlen:
            for i in range(mlen+1, nlen):
                outFile.write(negatives[i])
    
    print("processed train data saved in " + dstTrainFile, " with ", 2*trainLen, " records" )

    with open(dstValidFile, writeFormat, newline='\n') as outFile:
        for i in range(trainLen+ 1, mlen):
            outFile.write(positives[i])
            outFile.write(negatives[i])

    print("processed validation data saved in " + dstValidFile, " with ", 2*(mlen- trainLen), " records" )

    return True


def train(dstTrainFile, dstValidFile, exeName, exeExtention):
    # assumes fasttext location is in Path variable of the running OS
    subprocess.check_call(["fasttext", "supervised", "-input", dstTrainFile, 
        "-output", exeName, "-lr", "1.0", "-epoch", "12", "-wordNgrams", "2",
        "-verbose", "2"])
    
    exeFile = exeName + "." + exeExtention

    command = "fasttext test " + exeName + "." + exeExtention + " " + dstValidFile
    print("command:", command)
    subprocess.check_call(command.split(), shell = False)

    return True


def interact(exeName, exeExtention):
    command = "fasttext predict "  + exeName + "." + exeExtention + " -" 
    subprocess.check_call(command.split(), shell = False)



if __name__ == "__main__":

    args = parseArgsnFlags()
    print("args:", args)
    
    if args.filename == "":
        print("no file name given")
        pass

    dataCol = 0
    labelCol = 0

    try:
        dataCol = int(args.datacol)
    except ValueError:
        print("datacol for -d flag is not valid int")
        sys.exit(1)

    try:
        labelCol = int(args.labelcol)
    except ValueError:
        print("labelcol for -l flag is not valid int")
        sys.exit(1)


    if process(args.filename, "w", "pdata.train", "pdata.valid", labelCol, dataCol ) == False:
        print("process fail")
        pass

    # if train("pdata.train", "pdata.valid", "abstractor", "bin") == False:
    #     print("train fail")
    #     pass

    # if args.interactive:
    #     interact("abstractor", "bin")
