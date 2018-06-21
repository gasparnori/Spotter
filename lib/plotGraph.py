import matplotlib.pyplot as plt
import numpy as np
#import seaborn as sns


def plotAllResults(px, py, speed, orientation, title):
    """plots the four analog outputs (x, y, speed, head orientation) for an object into one figure"""
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
    plt.title("head orientation (degrees)")
    plt.ylim([0, 360])
    plt.plot(orientation)
    plt.show()

def PlotFirstOrder(px, py, orientation,  title, txt):
    fontS = 20  # fontsize for all text
    if len(orientation)>0:
        fig, pl= plt.subplots(2, 1, True, False, True)
        pl[0].set_title("Position: x (blue), y (green)", fontsize=fontS)
        pl[0].set_ylabel("pixels", fontsize=fontS)
        pl[0].set_ylim([0, 640])
        pl[0].plot(px, 'b')
        pl[0].plot(py, 'g')
        pl[1].set_title("head orientation", fontsize=fontS)
        # plt.tight_layout()
        d = np.zeros(shape=(200, len(orientation)))
        d[:, 0:len(orientation)] = np.asmatrix(orientation)
        heatmap = pl[1].imshow(d, cmap='hsv', aspect='auto')
        heatmap.axes.get_xaxis().set_visible(False)
        heatmap.axes.get_yaxis().set_visible(False)
        plt.colorbar(heatmap, orientation='horizontal')

    else:
        fig, pl=plt.subplots(1, 1, False, False, True)
        pl.set_title("Position: x (blue), y (green)", fontsize=fontS)
        pl.set_ylabel("pixels", fontsize=fontS)
        pl.set_ylim([0, 640])
        pl.plot(px, 'b')
        pl.plot(py, 'g')

def PlotSecondOrder(speed, mov_dir, ang_vel, title, txt):
    fontS = 20  # fontsize for all text
    if len(ang_vel) > 0:
        fig, pl = plt.subplots(3, 1, True, False, True)
        pl[0].set_title("Speed", fontsize=fontS)
        pl[0].set_ylabel("speed [px/ms]", fontsize=fontS)
        pl[0].plot(speed)

        pl[1].set_title("Angular Velocity of Head Movement", fontsize=fontS)
        pl[1].set_ylabel("[degrees/ms]", fontsize=fontS)
        pl[1].plot(ang_vel)

        pl[2].set_title("Movement Direction (degrees)", fontsize=fontS)
        d = np.zeros(shape=(200, len(mov_dir)))
        d[:, 0:len(mov_dir)] = np.asmatrix(mov_dir)

        heatmap = pl[2].imshow(d, cmap='hsv', aspect='auto')
        heatmap.axes.get_xaxis().set_visible(False)
        heatmap.axes.get_yaxis().set_visible(False)

        plt.colorbar(heatmap, orientation='horizontal')


    else:
        fig, pl = plt.subplots(2, 1, False, False, True)
        pl[0].set_title("Speed", fontsize=fontS)
        pl[0].set_ylabel("speed [px/ms]", fontsize=fontS)
        pl[0].plot(speed)
        # can be calculated from one LED as well
        pl[1].set_title("Movement Direction", fontsize=fontS)
        d = np.zeros(shape=(200, len(mov_dir)))
        d[:, 0:len(mov_dir)] = np.asmatrix(mov_dir)

        heatmap = pl[1].imshow(d, cmap='hsv', aspect='auto')
        heatmap.axes.get_xaxis().set_visible(False)
        heatmap.axes.get_yaxis().set_visible(False)

        plt.colorbar(heatmap, orientation='horizontal')
        plt.tight_layout()

def PlotAll(px, py, speed, orientation, mov_dir, ang_vel, title, txt):
    fontS = 10  # fontsize for all text
    if len(orientation) > 0 and len(ang_vel)>0:
        fig, pl = plt.subplots(5, 1, True, False, True)
        pl[0].set_title("Position: x (blue), y (green)", fontsize=fontS)
        pl[0].set_ylabel("pixels", fontsize=fontS)
        pl[0].set_ylim([0, 640])
        pl[0].plot(px, 'b')
        pl[0].plot(py, 'g')
        pl[1].set_title("Head Orientation (degrees)", fontsize=fontS)
        # plt.tight_layout()
        d = np.zeros(shape=(200, len(orientation)))
        d[:, 0:len(orientation)] = np.asmatrix(orientation)
        heatmap = pl[1].imshow(d, cmap='hsv', aspect='auto')
        heatmap.axes.get_xaxis().set_visible(False)
        heatmap.axes.get_yaxis().set_visible(False)
        #plt.colorbar(heatmap, orientation='horizontal')

        pl[2].set_title("Speed", fontsize=fontS)
        pl[2].set_ylabel("speed [px/ms]",  fontsize=fontS)
        pl[2].plot(speed)

        pl[3].set_title("Angular Velocity of Head Movement", fontsize=fontS)
        pl[3].set_ylabel("ang. velocity  [deg/ms]",  fontsize=fontS)
        pl[3].plot(ang_vel)

        pl[4].set_title("Movement Direction", fontsize=fontS)
        d = np.zeros(shape=(200, len(mov_dir)))
        d[:, 0:len(mov_dir)] = np.asmatrix(mov_dir)

        heatmap = pl[4].imshow(d, cmap='hsv', aspect='auto')
        heatmap.axes.get_xaxis().set_visible(False)
        heatmap.axes.get_yaxis().set_visible(False)

        plt.colorbar(heatmap, orientation='horizontal')


    else:
        fig, pl = plt.subplots(3, 1, False, False, True)
        pl[0].set_title("Position: x (blue), y (green)", fontsize=fontS)
        pl[0].set_ylabel("pixels", fontsize=fontS)
        pl[0].set_ylim([0, 640])
        pl[0].plot(px, 'b')
        pl[0].plot(py, 'g')
        pl[1].set_title("Speed", fontsize=fontS)
        pl[1].set_ylabel("speed [px/ms]",  fontsize=fontS)
        pl[1].plot(speed)
        #can be calculated from one LED as well
        pl[2].set_title("Movement Direction", fontsize=fontS)
        d = np.zeros(shape=(200, len(mov_dir)))
        d[:, 0:len(mov_dir)] = np.asmatrix(mov_dir)

        heatmap = pl[2].imshow(d, cmap='hsv', aspect='auto')
        heatmap.axes.get_xaxis().set_visible(False)
        heatmap.axes.get_yaxis().set_visible(False)

        plt.colorbar(heatmap, orientation='horizontal')
        plt.tight_layout()


def PlotAllInOne(px, py, speed, orientation, mov_dir, ang_vel, title, txt, txt2):
    print txt
    print txt2
    PlotFirstOrder(px, py, orientation, title, txt)
    PlotSecondOrder(speed, mov_dir, ang_vel, title, txt)