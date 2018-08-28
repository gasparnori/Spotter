"""
Created on 13/08/2018
@author: <Nora Gaspar> nori.nagyonsok@gmail.com
This file is not part of Spotter, but these are helper functions to open the Spotter generated plot files.
"""
import matplotlib.pyplot as plt
import numpy as np
import time
import math
import matplotlib.image as mpimg
# import seaborn as sns
import scipy.io

#Write your path and file name here
path = "C:/Users/Owner/Documents/Spotter Article/"
file = "plot_graphs20180805_1847.dat"


def loadfromFile(path, filename):
    """Loads one or two objects from the .dat file"""
    obj0 = {}
    obj1 = {}
    dict = {}
    scipy.io.loadmat(path + file, dict)

    if 'object0' in dict:
        obj0['x'] = dict['object0']['px'][0][0][0]
        obj0['y'] = dict['object0']['py'][0][0][0]
        obj0['theta'] = dict['object0']['orientation'][0][0][0]
        obj0['time'] = dict['object0']['time'][0][0][0]
        obj0['movdir'] = dict['object0']['mov_dir'][0][0][0]
        obj0['speed'] = dict['object0']['speed'][0][0][0]
        obj0['angvel'] = dict['object0']['ang_vel'][0][0][0] * 10

    if 'object1' in dict:
        obj1['x'] = dict['object1']['px'][0][0][0]
        obj1['y'] = dict['object1']['py'][0][0][0]
        obj1['theta'] = dict['object1']['orientation'][0][0][0]
        obj1['time'] = dict['object1']['time'][0][0][0]
        obj1['movdir'] = dict['object1']['mov_dir'][0][0][0]
        obj1['speed'] = dict['object1']['speed'][0][0][0]
        obj1['angvel'] = dict['object1']['ang_vel'][0][0][0]
    return obj0, obj1


def PlotTogether(px, py, orientation, speed, mov_dir, ang_vel, times, title):
    fontS = 20  # fontsize for all text

    nr = 5 if len(orientation) > 0 else 3
    fig, pl = plt.subplots(nr, 1, True, False, True)

    fig.suptitle(title, fontsize=fontS)
    pl[0].set_title("Position: x (blue), y (green)", fontsize=fontS)
    pl[0].set_ylabel("pixels", fontsize=fontS)
    pl[0].set_ylim([0, 640])
    pl[0].plot(times, px, 'b')
    pl[0].plot(times, py, 'g')

    pl[1].set_title("Speed", fontsize=fontS)
    pl[1].set_ylabel("speed [px/s]", fontsize=fontS)
    pl[1].plot(times, speed)

    pl[2].set_title("Movement Direction (degrees)", fontsize=fontS)
    d = np.zeros(shape=(200, len(mov_dir)))
    d[:, 0:len(mov_dir)] = np.asmatrix(mov_dir)
    heatmap = pl[2].imshow(d, cmap='hsv', aspect='auto')
    heatmap.axes.get_xaxis().set_visible(False)
    heatmap.axes.get_yaxis().set_visible(False)

    if len(orientation) > 0:
        pl[3].set_title("head orientation", fontsize=fontS)
        # plt.tight_layout()
        d = np.zeros(shape=(200, max(times)))
        d[:, 0:times[0] - 1] = orientation[0]
        for i in range(1, len(times)):
            d[:, times[i - 1]:times[i] - 1] = orientation[i]
        # d[:, 0:len(orientation)] = np.asmatrix(orientation)
        heatmap = pl[3].imshow(d, cmap='hsv', aspect='auto')
        heatmap.axes.get_xaxis().set_visible(False)
        heatmap.axes.get_yaxis().set_visible(False)

    if len(ang_vel) > 0:
        pl[4].set_title("Angular Velocity of Head Movement", fontsize=fontS)
        pl[4].set_ylabel("[degrees/s]", fontsize=fontS)
        pl[4].plot(times, ang_vel)
        # plt.tight_layout()


def PlotFirstOrder(px, py, orientation, times, title, txt):
    fontS = 20  # fontsize for all text
    if len(orientation) > 0:
        fig, pl = plt.subplots(2, 1, True, False, True)
        fig.suptitle(title, fontsize=fontS)
        pl[0].set_title("Position: x (blue), y (red)", fontsize=fontS)
        pl[0].set_ylabel("[pixels]", fontsize=fontS)
        pl[0].set_ylim([0, 640])
        pl[0].plot(times, px, '#0f2bc6')
        pl[0].plot(times, py, '#ce7152')
        pl[1].set_title("head orientation [degrees]", fontsize=fontS)
        # plt.tight_layout()
        d = np.zeros(shape=(200, max(times)))
        d[:, 0:times[0] - 1] = orientation[0]
        for i in range(1, len(times)):
            d[:, times[i - 1]:times[i] - 1] = orientation[i]
        # d[:, 0:len(orientation)] = np.asmatrix(orientation)
        heatmap = pl[1].imshow(d, cmap='hsv', aspect='auto')
        heatmap.axes.get_xaxis().set_visible(False)
        heatmap.axes.get_yaxis().set_visible(False)
        # plt.colorbar(heatmap, orientation='horizontal')

    else:
        fig, pl = plt.subplots(1, 1, False, False, True)
        fig.suptitle(title, fontsize=fontS)
        pl.set_title("Position: x (blue), y (red)", fontsize=fontS)
        pl.set_ylabel("[pixels]", fontsize=fontS)
        pl.set_ylim([0, 640])
        pl[0].plot(times, px, '#0f2bc6')
        pl[0].plot(times, py, '#ce7152')
        plt.tight_layout()


def PlotSecondOrder(speed, mov_dir, ang_vel, times, title, txt):
    fontS = 20  # fontsize for all text
    if len(ang_vel) > 0:
        fig, pl = plt.subplots(3, 1, True, False, True)
        fig.suptitle(title, fontsize=fontS)
        pl[0].set_title("Speed", fontsize=fontS)
        pl[0].set_ylabel("[px/s]", fontsize=fontS)
        pl[0].plot(times, speed)

        pl[1].set_title("Angular Velocity of Head Movement", fontsize=fontS)
        pl[1].set_ylabel("[degrees/s]", fontsize=fontS)
        pl[1].plot(times, ang_vel)

        pl[2].set_title("Movement Direction [degrees]", fontsize=fontS)
        d = np.zeros(shape=(200, len(mov_dir)))
        d[:, 0:len(mov_dir)] = np.asmatrix(mov_dir)

        heatmap = pl[2].imshow(d, cmap='hsv', aspect='auto')
        heatmap.axes.get_xaxis().set_visible(False)
        heatmap.axes.get_yaxis().set_visible(False)

        # plt.colorbar(heatmap, orientation='horizontal')


    else:
        fig, pl = plt.subplots(2, 1, False, False, True)
        fig.suptitle(title, fontsize=fontS)
        pl[0].set_title("Speed", fontsize=fontS)
        pl[0].set_ylabel("speed [px/s]", fontsize=fontS)
        pl[0].plot(speed)
        # can be calculated from one LED as well
        pl[1].set_title("Movement Direction [degrees]", fontsize=fontS)
        d = np.zeros(shape=(200, len(mov_dir)))
        d[:, 0:len(mov_dir)] = np.asmatrix(mov_dir)

        heatmap = pl[1].imshow(d, cmap='hsv', aspect='auto')
        heatmap.axes.get_xaxis().set_visible(False)
        heatmap.axes.get_yaxis().set_visible(False)

        # plt.colorbar(heatmap, orientation='horizontal')
        plt.tight_layout()


def PlotXYSpeedTheta(x1, y1, sp1, x2, y2, sp2, theta1, theta2, times):
    fontS = 18
    fig, pl = plt.subplots(3, 1, gridspec_kw={'height_ratios': [3, 1, 1]})
    # fig.suptitle("Position and speed with and without Kalman filtering", fontsize=fontS)

    pl[0].set_title("Results of Kalman filtering", fontsize=fontS)
    pl[0].set_ylabel("[px]", fontsize=12)
    pl[0].set_ylim([100, 250])
    pl[0].set_xlim([21500, 26500])
    # pl[0].plot(times, sp2, '#544d4d')
    # pl[0].plot(times, sp1, '#000000')
    xbefore, = pl[0].plot(times, x2, '#3ec6d6', label='X before')
    xafter, = pl[0].plot(times, x1, '#0f2bc6', label='X after')
    ybefore, = pl[0].plot(times, y2, '#ce7152', label='Y before')
    yafter, = pl[0].plot(times, y1, '#af050d', label='Y after')
    pl[0].legend(handles=[xbefore, xafter, ybefore, yafter], loc='upper left', fontsize=10)

    pl[1].set_ylabel("[px/s]", fontsize=12)
    pl[1].set_xlim([21500, 26500])
    pl[1].set_ylim([0, 500])
    sp_before, = pl[1].plot(times, sp2, '#8fa1a3', label="v before")
    sp_after, = pl[1].plot(times, sp1, '#00cc00', label="v after")
    pl[1].legend(handles=[sp_before, sp_after], loc='upper left', fontsize=10)

    pl[2].set_title("head orientation before (above) and after (below)", fontsize=14)
    d = np.ones(shape=(300, times[1421] - times[1215]))

    d[0:150, 0:times[1215] - 21500] = theta2[0]
    d[150:, 0:times[1215] - 21500] = theta1[0]
    for i in range(1216, 1422):
        d[0:150, times[i - 1] - 21500:times[i] - 21500] = math.fmod(theta2[i] + 360, 360)
        d[150:, times[i - 1] - 21500:times[i] - 21500] = math.fmod(theta1[i] + 360, 360)
    heatmap = pl[2].imshow(d, cmap='hsv', aspect='auto')
    heatmap.axes.get_yaxis().set_visible(False)
    # heatmap.axes.get_xaxis().set_visible(False)

    pl[0].axes.get_xaxis().set_visible(False)
    pl[1].axes.get_xaxis().set_visible(False)
    pl[2].set_xlabel("[ms]", fontsize=12)

    plt.tight_layout()


def PlotXYSpeed(x1, y1, sp1, x2, y2, sp2, times):
    fontS = 18
    fig, pl = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})

    pl[0].set_title("Results of Kalman filtering", fontsize=fontS)

    pl[0].set_ylim([100, 250])
    pl[0].set_ylabel("[px]", fontsize=12)
    pl[0].set_xlim([21500, 26500])
    xbefore, = pl[0].plot(times, x2, '#3ec6d6', label='X before')
    xafter, = pl[0].plot(times, x1, '#0f2bc6', label='X after')
    ybefore, = pl[0].plot(times, y2, '#ce7152', label='Y before')
    yafter, = pl[0].plot(times, y1, '#af050d', label='Y after')
    pl[0].axes.get_xaxis().set_visible(False)
    pl[0].legend(handles=[xbefore, xafter, ybefore, yafter], loc='upper left', fontsize=12)

    pl[1].set_xlim([21500, 26500])
    pl[1].set_ylim([0, 500])
    pl[1].set_ylabel("[px/s]", fontsize=12)
    pl[1].set_xlabel("[ms]", fontsize=12)
    sp_before, = pl[1].plot(times, sp2, '#8fa1a3', label="v before")
    sp_after, = pl[1].plot(times, sp1, '#00cc00', label="v after")
    pl[1].legend(handles=[sp_before, sp_after], loc='upper left', fontsize=12)

    plt.tight_layout()


def PlotAll(x, y, sp, angvel, orientation, mov_dir, times):
    fontS = 18
    fig, pl = plt.subplots(3, 2, gridspec_kw={'height_ratios': [6, 1, 1], 'width_ratios': [7, 1]})
    # fig.suptitle("Position with and without Kalman filtering", fontsize=fontS)

    pl[0][0].set_title("Object parameters", fontsize=fontS)
    # pl.set_ylabel("[pixels]", fontsize=fontS)
    pl[0][0].set_ylim([0, 640])
    pl[0][0].set_xlim([0, 50000])
    #pl[0][0].set_xlabel("[ms]")
    speed, = pl[0][0].plot(times, sp, '#000000', label='Speed [px/s]')
    px, = pl[0][0].plot(times, x, '#463fff', label='X position [px]')
    py, = pl[0][0].plot(times, y, '#fe3152', label='Y position [px]')
    av, = pl[0][0].plot(times, angvel, '#a1a1a1', label='Angular velocity [deg/s]')
    pl[0][0].legend(handles=[px, py, speed, av], loc='upper left', fontsize=12)
    #pl[0][0].axes.get_xaxis().set_visible(False)

    pl[1][0].set_title("Head Orientation [degrees]", fontsize=14)
    pl[1][0].set_xlim([0, 50000])
    # plt.tight_layout()
    d = np.zeros(shape=(200, max(times)))
    d[:, 0:times[0] - 1] = orientation[0]
    for i in range(1, len(times)):
        d[:, times[i - 1]:times[i]] = orientation[i]
    pl[1][0].plot(times, angvel, '#a1a1a1', label='Angular velocity [deg/s]')

    heatmap = pl[1][0].imshow(d, cmap='hsv', aspect='auto', origin='lower')
    #heatmap.axes.get_xaxis().set_visible(False)
    heatmap.axes.get_yaxis().set_visible(False)

    pl[2][0].set_title("Movement Direction", fontsize=14)
    pl[2][0].set_xlim([0, 50000])
    md = np.zeros(shape=(100, max(times)))
    pl[2][0].plot(times, sp, '#000000', label='Speed [px/s]')
    md[:, 0:times[0]] = mov_dir[0]
    for i in range(1, len(times)):
        md[:, times[i - 1]:times[i]] = mov_dir[i]

    heatmap = pl[2][0].imshow(md, cmap='hsv', aspect='auto', origin='lower')
    #heatmap.axes.get_xaxis().set_visible(False)
    heatmap.axes.get_yaxis().set_visible(False)

    pl[0][1].set_visible(False)
    pl[1][1].set_visible(False)
    pl[2][1].set_visible(False)
    #cbaxes = fig.add_axes([0.9, 0.1, 0.03, 0.8])
    #cb = plt.colorbar(heatmap, cax=cbaxes)
    plt.tight_layout()


obj0, obj1 = loadfromFile(path, file)
txt = "Total number of frames: " + str(len(obj1['theta'])) + " Number of missed frames: " + str(
    np.count_nonzero(obj1['theta'] == 0))

# PlotFirstOrder(obj0['x'], obj0['y'], obj0['theta'],obj0['time'], 'Object 0', "")
# PlotSecondOrder(obj0['speed'], obj0['movdir'], obj0['angvel'],obj0['time'], 'Object 0', "")

# PlotFirstOrder(obj1['x'], obj1['y'], obj1['theta'],obj1['time'], 'Object 1', "")
# PlotSecondOrder(obj1['speed'], obj1['movdir'], obj1['angvel'],obj1['time'], 'Object 0', "")
# (px,py,orientation, speed, movdir, angvel, time, title):

#PlotXYSpeedTheta(obj0['x'], obj0['y'], obj0['speed'], obj1['x'], obj1['y'], obj1['speed'], obj0['theta'], obj1['theta'],
#                 obj0['time'])
PlotXYSpeed(obj0['x'], obj0['y'], obj0['speed'], obj1['x'], obj1['y'], obj1['speed'], obj0['time'])
#PlotAll(obj0['x'], obj0['y'], obj0['speed'], obj0['angvel'], obj0['theta'], obj0['movdir'], obj0['time'])
# PlotAll(obj1['x'], obj1['y'], obj1['speed'], obj1['angvel'], obj1['theta'], obj1['movdir'], obj1['time'])
plt.show()

print txt