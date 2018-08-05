#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 09:28:37 2012
@author: <Ronny Eichler> ronny.eichler@gmail.com
edited: Nora Gaspar nori.nagyonsok@gmail.com

Tracks colored spots in images or series of images

Usage:
    tracker.py --source SRC [options]
    tracker.py -h | --help

Options:
    -h --help        Show this screen
    -s --source SRC  Source, path to file or integer device ID [default: 0]
    -S --Serial      Serial port to uC [default: None]
    -c --continuous  Track spots over time, not frame by frame
    -D --DEBUG       Verbose debug output
    -H --Headless    No Interface

"""

import cv2
import logging
import time
import sys
import numpy as np
import math

import lib.utilities as utils
import lib.geometry as geom
import trackables as trkbl
from lib.docopt import docopt

DEBUG = False #True

class tracked_blob:
    def __init__(self, cnt, last_coord, offset_x, offset_y, range_area):
        try:
            self.cnt=cnt
            self.area = cv2.contourArea(self.cnt.astype(int))
            if self.area<range_area[0]:
                self.cx=None
                self.cy=None
                self.dist=None
                #print "empty area"
            else:
                moment = cv2.moments(cnt.astype(int))
                self.cx = math.ceil(moment['m10'] / moment['m00']) + offset_x
                self.cy = math.ceil(moment['m01'] / moment['m00']) + offset_y
                self.dist = geom.distance(last_coord, (self.cx, self.cy)) if (last_coord is not None) else 0

        except:
            print "error", sys.exc_info()[0]

class Tracker:
    """ Performs tracking and returns positions of found LEDs """
    frame = None
    scale = 1.0
    contour=None
    max_x=639
    max_y=379
    fps=190.0

    def __init__(self, adaptive_tracking=False):

        self.log = logging.getLogger(__name__)

        self.oois = [] #objects of interest
        self.rois = [] #regions of interest
        self.leds = [] #markers
        self.bspots= [] #blind spots
        self.adaptive_tracking = adaptive_tracking

    def add_blindspot(self, mask_list, label):
        #mask = trkbl.Mask('rectangle', None, 'label')
        bs=trkbl.BlindSpot(mask_list, label)
        self.log.debug("Added blindspot %s", bs.label)
        self.bspots.append(bs)
        return bs

    def remove_blindspot(self, bs):
        try:
            #print bs
            #print

            #del self.bspots.shapes[:]
            label=bs.label
            del bs.masks[:]
            self.bspots.remove(bs)
            self.log.debug("Blindspot removed %s ", label)
        except ValueError:
            self.log.error("Blind spot to be removed not found")

    def add_led(self, label, range_hue, range_sat, range_val, range_area, fixed_pos=False, linked_to=None, filter_dim=4, R=None, Q=None, filtering_enabled=False, guessing_enabled = False):
        if self.adaptive_tracking:
            roi = trkbl.Shape('rectangle', None, None)
        else:
            roi = trkbl.Shape('rectangle', None, None)
        led = trkbl.LED(label, range_hue, range_sat, range_val, range_area, fixed_pos, linked_to, roi, self.max_x, self.max_y, filter_dim, R, Q, filtering_enabled, guessing_enabled, self.fps)
        self.leds.append(led)
        self.log.debug("Added marker %s", led)
        return led

    def remove_led(self, led):
        try:
            self.log.debug("Removing marker %s", led)
            self.leds.remove(led)
            for o in self.oois:
                if led in o.linked_leds:
                    o.linked_leds.remove(led)
        except ValueError:
            self.log.error("marker to be removed not found")

    def add_ooi(self, led_list, label, traced=False, tracked=True, magnetic_signals=None):
        ooi = trkbl.ObjectOfInterest(led_list, label, traced, tracked, magnetic_signals, self.max_x, self.max_y)
        self.oois.append(ooi)
        self.log.debug("Added object %s", ooi)
        return ooi

    def remove_ooi(self, ooi):
        try:
            self.oois.remove(ooi)
            for roi in self.rois:
                roi.refresh_slot_list()
        except ValueError:
            self.log.error("Object to be removed not found")

    def add_roi(self, shape_list, label, color=None, magnetic_objects=None):
        roi = trkbl.RegionOfInterest(shape_list, label, color, self.oois, magnetic_objects)
        self.rois.append(roi)
        self.log.debug("Added region %s", roi)
        return roi

    def remove_roi(self, roi):
        try:
            del roi.shapes[:]
            self.rois.remove(roi)
        except ValueError:
            self.log.error("Region to be removed not found")

    def trackFPS(self, pin):
        f=trkbl.fpsTestSignal(pin)
        return f

    def mask_blindspots(self, frame):
        """
        this function draws black mask directly on the frame, overwriting the original values (for example hiding an object)
        further development: look them up from a lookup table instead of this solution
        """
        for b in self.bspots:
            for m in b.masks:
                if m.shape=='line' and m.active:
                    cv2.line(frame.img, m.p1, m.p2, (0, 0, 0), 3)
                if m.shape== 'rectangle' and m.active:
                    cv2.rectangle(frame.img, m.p1, m.p2, (0, 0, 0), -1)
                if m.shape== 'circle' and m.active:
                    cv2.circle(frame.img, m.p1, m.radius, (0, 0, 0), -1)
        return frame

    def track_marker(self, frame, method='hsv_thresh', scale=1.0, elapsedtime=5):
        """
        Intermediate method selecting tracking method and separating those
        tracking methods from the frames stored in the instantiated Tracker

        :param:scale
            Resize frame before tracking, computation decreases scale^2.
        """
        self.fps=frame.fps

        self.scale = scale*1.0  # float
        if self.scale > 1.0:
            self.scale = 1.0

#        # conversion to HSV before dilation causes artifacts!
        # dilate bright spots
#        kernel = np.ones((3,3), 'uint8')

        # smooth the image?
        #kernel = np.ones((5, 5), np.float32)/10
        #frame.img = cv2.filter2D(frame.img, -1, kernel)

        if method == 'hsv_thresh':
            if self.scale >= 1.0:
                self.frame = cv2.cvtColor(frame.img, cv2.COLOR_BGR2HSV)
            else:
                # TODO: Performance impact of INTER_LINEAR vs. INTER_NEAREST?
                self.frame = cv2.cvtColor(cv2.resize(frame.img, (0, 0), fx=self.scale, fy=self.scale,
                                                     interpolation=cv2.INTER_NEAREST), cv2.COLOR_BGR2HSV)



            height, width, channels = self.frame.shape
            self.max_x=width
            self.max_y=height

            #checks the location of all LED's chooses the best, and applies kalman filter on that
            for led in self.leds:
                if led.detection_active:
                    self.track_thresholds(self.frame, led, elapsedtime)
                else:
                    led.pos_hist.append(None)

    def track_thresholds(self, hsv_frame, l, elapsedtime=5):
        """
        Tracks LEDs from a list in a HSV frame by thresholding
        hue, saturation, followed by thresholding for each LEDs hue.
        Large enough contours will have coordinates returned, or None
        """
        r_hue = l.range_hue
        r_sat = l.range_sat
        r_val = l.range_val
        r_area = (l.range_area[0]*self.scale**2, l.range_area[1]*self.scale**2)

        # determine array slices if adaptive tracking is used
        if (l.adaptive_tracking and self.adaptive_tracking) \
           and l.search_roi is not None and l.search_roi.points is not None:
            (ax, ay), (bx, by) = l.search_roi.points
            h, w = hsv_frame.shape[0:2]
            ax = int(ax * self.scale) if ax >= 0 else 0
            bx = int(bx * self.scale) if (bx <= w-1) else w-1
            ay = int(ay * self.scale) if ay >= 0 else 0
            by = int(by * self.scale) if by <= h-1 else h-1

            frame = hsv_frame[ay:by, ax:bx, :]
            frame_offset = True
        else:
            frame_offset = False
            frame = hsv_frame

        # if range[0] > range[1], i.e., color is red and wraps around
        invert_range = False if not r_hue[0] > r_hue[1] else True

        # All colors except red
        if not invert_range:
            lower_bound = np.array([r_hue[0], r_sat[0], r_val[0]], np.uint8)
            upper_bound = np.array([r_hue[1], r_sat[1], r_val[1]], np.uint8)
            ranged_frame = cv2.inRange(frame, lower_bound, upper_bound)

        # Red hue requires double thresholding due to wraparound in hue domain
        else:
            # min-180 (or, 255)
            lower_bound = np.array([r_hue[0], r_sat[0], r_val[0]], np.uint8)
            upper_bound = np.array([179, r_sat[1], r_val[1]], np.uint8)
            ranged_frame = cv2.inRange(frame, lower_bound, upper_bound)
            # 0-max (or, 255)
            lower_bound = np.array([0, r_sat[0], r_val[0]], np.uint8)
            upper_bound = np.array([r_hue[1], r_sat[1], r_val[1]], np.uint8)
            red_range = cv2.inRange(frame, lower_bound, upper_bound)
            # combine both ends for complete mask
            ranged_frame = cv2.bitwise_or(ranged_frame, red_range)

        # find largest contour that is >= than minimum area
        ranged_frame = cv2.dilate(ranged_frame, np.ones((3, 3), np.uint8))
        #if l.linked_to() is not None
        prev_location=l.last_stable
        # if l.linked_to is None:
        #     prev_location = l.last_stable
        #     #prev_location= l.pos_hist[-1] if len(l.pos_hist)>0 else None
        # else:
        #     prev_location=l.linked_to.pos_hist[-1] if len(l.linked_to.pos_hist)>0 else None
        offset_x= ax if frame_offset else 0
        offset_y=ay if frame_offset else 0
        l.before_filter, self.contour = self.find_best_coordinates(ranged_frame, r_area, prev_location, offset_x, offset_y, self.scale)
        l.elapsedtime=elapsedtime
        l.filterPosition()

    @staticmethod
    def find_best_coordinates(frame, range_area, last_coord, offset_x, offset_y, scale):
        """
        Return contour with largest area. Returns None if no contour within
        admissible range_area is found.
        """
        contours, hierarchy = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        largest_area = range_area[0]    # starts from the minimum area that we are looking for
        max_area = range_area[1] if range_area[1] > 0 else 50000  #if the maximum is 0 --> max_area is bigger than the frame size
        best_cnt = None
        last_measured = None
        best_coord=None
        best_distance=10000
        #print "number of contours: ", len(contours)
        blobs=[tracked_blob(cnt, last_coord, offset_x, offset_y, range_area) for cnt in contours]
        if len(blobs)==0:
            return None, None
        elif len(blobs) == 1:
           # best_coord=(blobs[0].cx, blobs[0].cy)
            if blobs[0].cx is not None and blobs[0].cy is not None:
                last_measured=(blobs[0].cx/scale, blobs[0].cy/scale)
            best_cnt=blobs[0].cnt
        else:
            for b in blobs:
                # if this blob is closer than the best contour with at lest 10 pixels, it chooses this one
                if b.dist is not None and (b.dist < best_distance-10):
                    largest_area = b.area
                    best_cnt = b.cnt
                    last_measured = (b.cx / scale, b.cy / scale)
                    best_distance = b.dist
                elif (b.area > largest_area and b.area < max_area): #b.area can't be None
                    largest_area = b.area
                    best_cnt = b.cnt
                    last_measured = (b.cx / scale, b.cy / scale)
                    best_distance=b.dist

        return last_measured, best_cnt

    def close(self):
        """ Nothing to do here. """
        self.log.debug('Closing tracker')

#############################################################
if __name__ == '__main__':                                  #
#############################################################
    pass
    ## Parsing CLI arguments
    #arg_dict = docopt( __doc__, version=None )
    #DEBUG = arg_dict['--DEBUG']
    #if DEBUG: print arg_dict
    #
    ## Run in command line without user interface to slow things down
    #GUI = not arg_dict['--Headless']
    #
    ## Instantiate frame source to get something to write
    #import grabber
    #frame_source = grabber.Grabber( arg_dict['--source'] )
    #fps = frame_source.fps
    #
    #tracker = Tracker( arg_dict['--Serial'] )
    #
    #tracker.add_led( 'red', ( 160, 5 ) )
    #tracker.add_led( 'sync', ( 15, 90 ), fixed_pos = True )
    #tracker.add_led( 'blue', ( 105, 135 ) )
    #
    #tracker.addObjectOfInterest( [tracker.leds[0],
    #                              tracker.leds[2]],
    #                              'MovingObject' )
    #
    #colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]
    #
    ## Main loop till EOF or Escape key pressed
    #ts = time.clock()
    #n = 0
    #key = 0
    #while frame_source.grab_next() and not ( key % 100 == 27 ):
    #    frame = frame_source.framebuffer.pop()
    #
    #    # tracker works with HSV frames, not BGR
    #    tracker.frame = cv2.cvtColor( frame, cv2.COLOR_BGR2HSV )
    #    tracker.trackLeds( tracker.frame, method = 'hsv_thresh' )
    #    tracker.ooi.updatePosition()
    #
    #    if not tracker.ooi.pos_hist[-1] == None:
    #        tracker.chatter.send(tracker.ooi.position)
    #
    #    for idx, led in enumerate( tracker.leds ):
    #        if not led.pos_hist[-1] == None:
    #            utils.drawCross( frame, led.pos_hist[-1], 5, colors[idx], gap = 3 )
    #
    #    # 0.12ms for 10, 0.5ms to draw 100 points
    #    utils.drawTrace( frame, tracker.ooi.pos_hist, 255, 100 )
    #
    #    # draw ROIs
    #    for r in tracker.rois:
    #        r.draw( frame )
    #
    #    if GUI:
    #        cv2.imshow( 'Tracker', frame )
    #        key = cv2.waitKey(1)
    #
    #    n += 1
    #
    ## Exiting gracefully
    #tt = time.clock() - ts
    #t_fps = n*1.0/tt
    #print 'Tracked ' + str(n) + ' frames in ' + str(tt) + 's, ' + str(t_fps) + ' fps'
    #frame_source.close()
    #sys.exit(0)
