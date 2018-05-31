import matplotlib.pyplot as plt

from itertools import cycle

cycol = cycle('bgrcmk')

class DummyData:
    X = [590,540,740,130,810,300,320,230,470,620,770,250]
    Y = [32,36,39,52,61,72,77,75,68,57,48,48]
    Y2 = [i+20 for i in Y]


def PlotPrecisionRecall(X, precisions, recalls, epochs, xMin, xMax, yMin, yMax, title, xLabel, yLabel):
    
    if isinstance(xMin, (int, float)) == False:
        print("xMin not int or float")
        return
    if isinstance(xMax, (int, float)) == False:
        print("xMax not int or float")
        return
    if isinstance(yMin, (int, float)) == False:
        print("yMin not int or float")
        return
    if isinstance(yMax, (int, float)) == False:
        print("yMax not int or float")
        return


    if len(precisions[0]) != len(recalls[0]):
        print("precision and recall items not same size")
        return
    plen = len(precisions[0])

    # plt.scatter(X,Y,s=60, c='red', marker='.')
    for i, p in enumerate(precisions):
        plotLabel = "precision and recall at epoch "+str(epochs[i])
        print("plotLabel:", plotLabel)
        plt.plot(X, p, c=next(cycol), marker='.')

        plt.text(X[plen-1], p[plen-1], plotLabel)
    
    for i, r in enumerate(recalls):

        plt.plot(X, r, c=next(cycol), marker='.')

        # if plen > 1:
        #     plotLabel = "recall at epoch "+str(epochs[i])
        #     plt.text(X[0], r[0], plotLabel)


    plt.xlim(xMin, xMax)
    plt.ylim(yMin, yMax)

    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.show()



# PlotPrecisionRecall(DummyData.X, DummyData.Y, DummyData.Y2)
