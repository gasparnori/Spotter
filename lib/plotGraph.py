import matplotlib.pyplot as plt
import numpy as np
import time
#import seaborn as sns
import scipy.io

#SAVE_PLOT_VALS=True

plot_val_path='./outputs/plot_graphs'

def PlotFirstOrder(px, py, orientation, times,  title, txt):
    fontS = 20  # fontsize for all text
    if len(orientation)>0:
        fig, pl= plt.subplots(2, 1, True, False, True)
        fig.suptitle(title, fontsize=fontS)
        pl[0].set_title("Position: x (blue), y (green)", fontsize=fontS)
        pl[0].set_ylabel("pixels", fontsize=fontS)
        pl[0].set_ylim([0, 640])
        pl[0].plot(times, px, 'b')
        pl[0].plot(times, py, 'g')
        pl[1].set_title("head orientation", fontsize=fontS)
        # plt.tight_layout()
        d = np.zeros(shape=(200, max(times)))
        d[:, 0:times[0]-1]=orientation[0]
        for i in range(1, len(times)):
             d[:, times[i - 1]:times[i]-1] = orientation[i]
        #d[:, 0:len(orientation)] = np.asmatrix(orientation)
        heatmap = pl[1].imshow(d, cmap='hsv', aspect='auto')
        heatmap.axes.get_xaxis().set_visible(False)
        heatmap.axes.get_yaxis().set_visible(False)
        plt.colorbar(heatmap, orientation='horizontal')

    else:
        fig, pl=plt.subplots(1, 1, False, False, True)
        fig.suptitle(title, fontsize=fontS)
        pl.set_title("Position: x (blue), y (green)", fontsize=fontS)
        pl.set_ylabel("pixels", fontsize=fontS)
        pl.set_ylim([0, 640])
        pl.plot(times, px, 'b')
        pl.plot(times, py, 'g')

def PlotSecondOrder(speed, mov_dir, ang_vel, times, title, txt):
    fontS = 20  # fontsize for all text
    if len(ang_vel) > 0:
        fig, pl = plt.subplots(3, 1, True, False, True)
        fig.suptitle(title, fontsize=fontS)
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
        fig.suptitle(title, fontsize=fontS)
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

def Plot_All(objects, SAVE_PLOT_VALS):

    if SAVE_PLOT_VALS:
        save_dict = {}
    if len(objects) > 0:
        obj = {}
        k = 0
        for o in objects:
            n = min(4000, len(o.pos_hist))
            txt = "Total number of frames: " + str(len(o.pos_hist[(-1 * n):])) + " Number of missed frames: " + str(
                o.pos_hist[(-1 * n):].count(None))
            txt2 = "Total number of frames: " + str(
                len(o.pos_hist[(-1 * n):])) + " Number of missed head orientations: " + str(
                o.orientation_hist[(-1 * n):].count(None))
            px = [p[0] if p is not None else 0 for p in o.pos_hist[(-1 * n):]]
            py = [p[1] if p is not None else 0 for p in o.pos_hist[(-1 * n):]]
            orientation = o.orientation_hist[(-1 * n):]
            speed = [p if p is not None else 0 for p in o.speed_hist[(-1 * n):]]
            mov_dir = o.mov_dir_hist[(-1 * n):]
            ang_vel = [p if p is not None else 0 for p in o.ang_vel_hist[(-1 * n):]]
            #times between frames
            times=o.time_hist[(-1 * n):]
            times[0] = int(times[0])
            for i in range (1, len(times)):
                times[i]=int(times[i]+times[i-1])


            PlotFirstOrder(px, py, orientation, times, ('Object ' + str(k)), txt)
            PlotSecondOrder(speed, mov_dir, ang_vel, times, ('Object ' + str(k)), txt)

            if SAVE_PLOT_VALS:
                orientation = [p if p is not None else 1000 for p in o.orientation_hist[(-1 * n):]]
                mov_dir = [p if p is not None else 1000 for p in o.mov_dir_hist[(-1 * n):]]
                save_dict['object' + str(k)] = {'px': px, 'py': py, 'speed': speed, 'orientation': orientation,
                                                'mov_dir': mov_dir, 'ang_vel': ang_vel, 'time': times}
            k = k + 1
        if SAVE_PLOT_VALS:
            #print "saving data"
            scipy.io.savemat(plot_val_path + time.strftime('%Y%m%d_%H%M', time.localtime()) + '.dat', save_dict)
        plt.show()

