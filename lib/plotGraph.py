import matplotlib.pyplot as plt
import numpy as np
#import seaborn as sns


def plotAllResults(px, py, speed, dir, title):
    """plots the four analog outputs (x, y, speed, head direction) for an object into one figure"""
    fig=plt.figure(title)
    fig.add_subplot(221)
    plt.title("coordinate X (pixel)")
    plt.ylim([0, 640])
    plt.plot(px)

    fig.add_subplot(222)
    plt.title("coordinate Y")
    plt.ylim([0, 640])
    plt.plot(py)

    fig.add_subplot(223)
    plt.title("speed (px/ms)")
    plt.plot(speed)

    fig.add_subplot(224)
    plt.title("head direction (degrees)")
    plt.ylim([0, 360])
    plt.plot(dir)
    plt.show()

def PlotAllInOne(px, py, speed, dir, title):
    fig = plt.figure(title)
    fig.add_subplot(211)
    plt.ylim([0, 640])
    plt.plot(px, 'b')
    plt.plot(py, 'g')
    plt.plot(speed, 'r')
    if len(dir)>0:
        fig.add_subplot(212)
        d = np.zeros(shape=(20, len(dir)))
        d[:, :] = np.asmatrix(dir)
        heatmap=plt.imshow(d, cmap='hsv')
        plt.colorbar(heatmap)
    plt.show()

def heatmap(dir):
    d=np.zeros(shape=(20, len(dir)))
    d[:, :] = np.asmatrix(dir)
    return d