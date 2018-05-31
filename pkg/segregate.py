import sys
import argparse
import subprocess
from extrapolate import PlotPrecisionRecall

X = []
precisions = []
recalls = []
epochs = []

class Conf:
    PrecisionLabel = "P@1"
    RecallLabel = "R@1"

def parseArgsnFlags():

    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--filename",
        help="file name of *.train, to be used as train data source", default="")

    return parser.parse_args()


def splitData(inFileName, outFileName, sz):
    print("infilename:", inFileName, " outFilename:", outFileName)
    with open(inFileName, newline='\n') as inFile:
        with open(outFileName,"w", newline='\n') as outFile:
            cnt = 0
            for l in inFile:
                outFile.write(l)
                cnt += 1
                if cnt == sz:
                    break
    return True


def train(dstTrainFile, dstValidFile, exeName, epoch, wordNgrams):
    # assumes fasttext location is in Path variable of the running OS
    subprocess.check_call(["fasttext", "supervised", "-input", dstTrainFile, 
        "-output", exeName, "-lr", "1.0", "-epoch", str(epoch), 
        "-wordNgrams", str(wordNgrams), "-verbose", "2"])
    
    command = "fasttext test " + exeName + ".bin " + dstValidFile
    res = subprocess.run(command.split(), shell = False, stdout=subprocess.PIPE).stdout.decode("utf-8")
    res = [s.strip() for s in res.splitlines()]
    
    pVal = 0
    rVal = 0

    for row in res:
        col = row.split('\t')
        print("lr:", row)
        if col[0] == Conf.PrecisionLabel:
            try:
                pVal = float(col[1])
            except:
                print("could not convert precision val to float")
                sys.exit(1)
        
        if col[0] == Conf.RecallLabel:
            try:
                rVal = float(col[1])
            except:
                print("could not convert precision val to float")
                sys.exit(1)
        
    return (pVal, rVal)


if __name__ == "__main__":

    args = parseArgsnFlags()

    if args.filename == "":
        print("no file name given")
        pass
    
    num_lines = sum(1 for line in open(args.filename))

    print("number of records:", num_lines)

    # num_lines = 300
    X = [sz for sz in range(100, num_lines, 100)]


    for epoch in range(10,21,10):
        p = []
        r = []
        for sz in range(100, num_lines, 100):

            print("sz:", sz)
            outFileName = "gen/exo" + str(sz) + ".train"

            if splitData(args.filename, outFileName, sz) == False:
                print("split data fail")
                sys.exit(1)
            
            pVal, rVal = train(outFileName, "exo.valid", "segabstractor", epoch, 2)

            p.append(pVal)
            r.append(rVal)

        precisions.append(p)
        recalls.append(r)
        epochs.append(epoch)


    print("X:", X)
    print("precisions:", precisions)
    print("recalls:", recalls)
    print("epochs:", epochs)

    PlotPrecisionRecall(X, precisions, recalls, epochs, 0, num_lines, 0.6, 1,
        "Relation of Precision and Recall with Data Size", "DataSet Size",
        "Precision (pink) and Recall (red)")

