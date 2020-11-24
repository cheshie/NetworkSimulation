import matplotlib.pyplot as plt
from os import getcwd
from sys import argv, path
path.append(getcwd() + "/..")
import nstrace

def plotgraph(x, y):
    plt.plot(x, y, 'r*')
    plt.show()
#


def prepare_data(pfile): 
    pfile  = open(argv[1], 'r')
    points = [float(x) for ln in pfile.readlines() for x in ln.split(' ')]
    return points[::2], points[1::2]
#

if __name__ == "__main__":
    if len(argv) != 2:
        exit()
    x, y = prepare_data(argv[1])
    plotgraph(x, y)
