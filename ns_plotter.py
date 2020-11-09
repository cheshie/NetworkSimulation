import nstrace
import matplotlib.pyplot as plt
from sys import argv


def plotgraph(x, y):
    plt.plot(x, y, 'r*')
    plt.show()



if __name__ == "__main__":
    if len(argv) != 2:
        exit()

    pfile  = open(argv[1], 'r')
    points = [float(x) for ln in pfile.readlines() for x in ln.split(' ')]
    plotgraph(points[::2], points[1::2])
