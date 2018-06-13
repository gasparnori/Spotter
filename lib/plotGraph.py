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

def PlotAllInOne(px, py, speed, dir, title, txt):
    fontS=18 #fontsize for all text
    fig = plt.figure(title)
    fig.add_subplot(311)
    plt.tight_layout()
    plt.title("Position: x (blue), y (green)",  fontsize=fontS)
    plt.ylabel("pixels",  fontsize=fontS)
    plt.ylim([0, 640])
    plt.plot(px, 'b')
    plt.plot(py, 'g')
    fig.add_subplot(312)
    plt.tight_layout()
    plt.title("velocity", fontsize=fontS)
    plt.ylabel("speed [px/ms]",  fontsize=fontS)
    plt.plot(speed, 'r')
    if len(dir)>0:
        fig.add_subplot(313)
        plt.title("head direction",  fontsize=fontS)
        plt.tight_layout()
        d = np.zeros(shape=(200, len(dir)))
        d[:, 0:len(dir)] = np.asmatrix(dir)
        heatmap=plt.imshow(d, cmap='hsv',aspect='auto')
        heatmap.axes.get_xaxis().set_visible(False)
        heatmap.axes.get_yaxis().set_visible(False)
        plt.colorbar(heatmap, orientation='horizontal')
    plt.figtext(0.5, 0, txt, horizontalalignment='center', verticalalignment='bottom', fontsize=fontS)
    plt.show()