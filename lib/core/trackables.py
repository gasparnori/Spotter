# -*- coding: utf-8 -*-
"""
Created on Tue Dec 04 21:41:19 2012
@author: <Ronny Eichler> ronny.eichler@gmail.com

Classes related to tracking.
"""

import math
import random
import lib.utilities as utils
import lib.geometry as geom
from PyQt4 import QtCore
import numpy as np
import lib.kalmanfilter as kfilter

SENSITIVITY = 0
HIST_BUFFER=5000    #number of values to be saved in the history arrays


class Shape:
    """ Geometrical shape that comprise ROIs. ROIs can be made of several
    independent shapes like two rectangles on either end of the track etc.
    Not sure about the color parameter, I think it better if all shapes in a
    ROI have the same color, to keep them together as one ROI.
    points: list of points defining the shape. Two for rectangle and circle,
    """

    # TODO: n-polygon and collision detection
    def __init__(self, shape, points=None, label=None):
        self.active = True
        self.selected = False
        self.collision_check = None

        self.shape = shape.lower()
        self.label = label

        self.points = points

        if shape == 'circle':
            # normalize the point positions based on radius,
            # second point is always to the right of the center

            self.points = [points[0], (int(points[0][0]), points[0][1] + self.radius)]
            self.collision_check = self.collision_check_circle
        elif shape == 'rectangle':
            self.collision_check = self.collision_check_rectangle
        elif shape == 'line':
            dx = math.fabs(self.points[0][0] - self.points[1][0])
            dy = math.fabs(self.points[0][1] - self.points[1][1])
            if dx==0:
                self.slope=1
            else:
                self.slope = (dy / dx)
            self.collision_check = self.collision_check_line

    def move(self, dx, dy):
        """ Move the shape relative to current position. """
        for i, p in enumerate(self.points):
            self.points[i] = (p[0] + dx, p[1] + dy)

    def move_to(self, points):
        """ Move the shape to a new absolute position. """
        self.points = points

    @property
    def radius(self):
        """ Calculate the radius of the circle. """
        return geom.distance(self.points[0], self.points[1])

    def collision_check_circle(self, point):
        """ Circle points: center point, one point on the circle. Test for
        collision by comparing distance between center and point of object with
        radius.
        """
        distance = geom.distance(self.points[0], point)
        if self.active and (distance <= self.radius):
            return True
        else:
            return False

    def collision_check_rectangle(self, point):
        """ Circle points: center point, one point on the circle. Test for
        collision by comparing distance between center and point of object with
        radius.
        """
        x_in_interval = (point[0] > min(self.points[0][0], self.points[1][0])) and \
                        (point[0] < max(self.points[0][0], self.points[1][0]))

        y_in_interval = (point[1] > min(self.points[0][1], self.points[1][1])) and \
                        (point[1] < max(self.points[0][1], self.points[1][1]))
        return self.active and x_in_interval and y_in_interval

    def collision_check_line(self, point):
        #stupid way to check collision with a line segment
        #step 1: check if the point falls within the rectangle
        x_in_interval = (point[0] > min(self.points[0][0], self.points[1][0])) and \
                        (point[0] < max(self.points[0][0], self.points[1][0]))

        y_in_interval = (point[1] > min(self.points[0][1], self.points[1][1])) and \
                        (point[1] < max(self.points[0][1], self.points[1][1]))
        #step2
        #check if the slope between one of the points and the new point is the same
        dx=math.fabs(point[0] - self.points[1][0])
        if dx>0:
            s = (math.fabs(point[1]- self.points[1][1]) /dx)
        else:
            s=1
        return (s==self.slope and self.active and x_in_interval and y_in_interval)

class Mask:
    """ Geometrical shape that comprise Blind spots. Blind spots can be made of several
    independent shapes like two rectangles on either end of the track etc. Almost the same as the Shapes"""

    def __init__(self, shape, points=None, label=None):
        self.active = True
        self.selected = False

        self.shape = shape.lower()
        self.label = label

        self.points = points
        self.p1=(int(points[0][0]), int(points[0][1]))
        self.p2 =(int(points[1][0]), int(points[1][1]))

    @property
    def radius(self):
        """ Calculate the radius of the circle. """
        return int(geom.distance(self.points[0], self.points[1]))

class Marker:
    """ General class holding a marker to be tracked with whatever tracking
    algorithm is appropriate.
    """

    def __init__(self):
        pass

class LED(Marker):
    """ Each instance is a spot defined by ranges in a color space. """

    def __init__(self, label, range_hue, range_sat, range_val, range_area, fixed_pos, linked_to, roi=None, max_x=639, max_y=379,  filter_dim=4, R=None, Q=None, filtering_enabled=False, guessing_enabled = False, fps=190.0):
        Marker.__init__(self)
        self.label = label
        self.detection_active = True
        self.marker_visible = True
        #kalman filter related flags
        self.guessing_enabled = guessing_enabled
        self.adaptiveKF=False
        self.filtering_enabled=filtering_enabled
        # marker description ranges
        self.range_hue = range_hue
        self.range_sat = range_sat
        self.range_val = range_val
        self.range_area = range_area
        self.max_x=max_x
        self.max_y=max_y

        #array of position history after the filter
        self.pos_hist = []
        #lets save memory
        #self.pos_hist = [None for x in range(1000)]
        #x,y coordinates before the kalman filter
        #self.last_measured=[]

        self.kalmanfilter=kfilter.KFilter(max_x, max_y, filter_dim, R, Q, fps)

        #initializing the last state of the filter
        #self.filterstate=[1,1,1,1]

        # Restrict tracking to a search window?
        self.adaptive_tracking = (roi is not None)
        # if so, where and which window?
        self.fixed_pos = fixed_pos
        self.search_roi = roi
        # List of linked markers, can be used for further constraints
        self.linked_to = linked_to

    @property
    def mean_hue(self):
        return utils.mean_hue(self.range_hue)

    @property
    def lblcolor(self):
        # mean color of range for labels/markers etc.
        return utils.HSVpix2RGB((self.mean_hue, 255, 255))

    @property
    def position(self):
        #first coordinate
        #if len(self.pos_hist)==1:
            #self.kalmanfilter.start_filter()
        return self.pos_hist[-1] if len(self.pos_hist) else None

    #this function is the one that essentially calculates the coordinates. called from tracker
    def filterPosition(self, elapsedtime, last_measured):
        #print last_measured
        if self.filtering_enabled:
            fpos= self.kalmanfilter.iterate_filter(elapsedtime, last_measured, guessing_enabled=self.guessing_enabled, adaptive=self.adaptiveKF)#, calibrating=False)
        #print fpos
            self.pos_hist.append(fpos)
        else:
            self.pos_hist.append(last_measured)

    # def recalibrateFilter(self):
    #     if len(self.pos_hist)>0:
    #         self.kalmanfilter.start_filter(self.pos_hist[-1])
    def reset(self):
        self.filtering_enabled=False
        self.kalmanfilter.stop_filter()
        #last_point=self.pos_hist[-1]
        self.pos_hist=self.pos_hist[-100:]
        self.kalmanfilter.start_filter(self.pos_hist[-1])
        self.filtering_enabled=True

class Slot:
    def __init__(self, label, slot_type, state=None, state_idx=None, ref=None):
        # While nice, should be used for style, not for identity testing
        # FIXME: Use instance comparisons vs. label comparisons
        self.label = label

        # analog (dac) or digital
        self.type = slot_type

        # The physical device pin
        self.pin = None
        self.pin_pref = None

        # reference to output value         must be a function!!!!
        self.state = state
        # index of output value if iterable
        # for example, the position could be x or y position
        # TODO: Unnecessary with proper use of @property decorators
        self.state_idx = state_idx
        self.ref = ref  # reference to object representing slot

    def attach_pin(self, pin):
        if self.pin and self.pin.slot:
            self.detach_pin()
        self.pin = pin
        self.pin.slot = self

    def detach_pin(self):
        print "we need to detach the signal here"
        #self.pin.slot.state=False
        self.pin.slot = None
        self.pin = None

    def __del__(self):
        print "Removing slot", self

class ObjectOfInterest:
    EVENFRAME = False
    """
    Object Of Interest. Collection of markers to be tracked together and
    report state and behavior, or trigger events upon conditions.
    """
    # TODO: Use general "markers" rather than LEDs specifically

    linked_leds = None

    tracked = True
    traced = False

    #analog_pos = False
    #analog_dir = False
    #analog_spd = False
    sp=0.0
    dir=0.0
    slots = None

    def __init__(self, led_list, label, traced=False, tracked=True, magnetic_signals=None, max_x=639, max_y=379):
        self.linked_leds = led_list
        self.label = label
        self.traced = traced
        self.tracked = tracked

        #position history (x,y)
        self.pos_hist = []
        #head orientation history
        self.orientation_hist = []
        #speed history
        self.speed_hist=[]
        #angular velocity history
        self.ang_vel_hist=[]
        #movement direction history
        self.mov_dir_hist=[]
        #elapsed time history
        self.time_hist=[]

        #self.orientation_coord_hist = []
        #self.guessing_enabled=False
        self.max_x=max_x
        self.max_y=max_y
        #self.headorientation=None

        # the slots for these properties/signals are greedy for pins
        if magnetic_signals is None:
            self.magnetic_signals = []
        else:
            self.magnetic_signals = magnetic_signals

        # listed order important. First come, first serve
        self.slots = [Slot('x position', 'dac', self.getPositionX),
                      Slot('y position', 'dac', self.getPositionY),
                      Slot('head orientation ', 'dac', self.getOrientation),
                      Slot('speed', 'dac', self.getSpeed),
                      Slot('movement direction ', 'dac', self.getMovementDir),
                      Slot('angular velocity', 'dac', self.getAngVel)]

    def update_state(self, elapsedtime):
        """Update marker search windows!"""
        self.append_position(elapsedtime)

        # go back max. n frames to find last position
        min_step = 25
        for p in range(0, min(len(self.pos_hist), 10)):
            if self.pos_hist[-p - 1] is not None:
                uidx = (p + 1) * min_step
                pos = map(int, self.pos_hist[-p - 1])
                roi = [(pos[0] - uidx, pos[1] - uidx), (pos[0] + uidx, pos[1] + uidx)]
                break
        else:  # search full frame
            roi = [(0, 0), (2000, 2000)]

        for l in self.linked_leds:
            if l.fixed_pos:
                # TODO: Movable marker ROIs
                l.search_roi.move_to([(0, 259), (100, 359)])
            else:
                l.search_roi.move_to(roi)

    def update_slots(self, chatter):
        for slot in self.slots:
            for ms in self.magnetic_signals:
                # Check that pin preferences are set correctly
                if slot.label == ms[0]:
                    if not slot.pin_pref == ms[1]:
                        slot.pin_pref = ms[1]

            if (slot.pin_pref is not None) and (slot.pin is None):
                # If pin pref and not connected to pin
                pins = chatter.pins_for_slot(slot)
                for pin in pins:
                    if pin.id == slot.pin_pref:
                        slot.attach_pin(pin)

    def update_values(self,elapsedtime):
        self.orientation()
        self.velocity(elapsedtime) #frame to frame interval for speed and direction calculation
        self.angularVelocity(elapsedtime)

    def append_position(self, elapsedtime):
        """Calculate position from detected markers linked to object."""
        if not self.tracked:
            return
        marker_positions = [f.pos_hist[-1] for f in self.linked_leds if len(f.pos_hist)]
        temp_position=geom.middle_point(marker_positions)
        #works as a FIFO
        if len(self.pos_hist)>=HIST_BUFFER:
            #pops the first element
            self.pos_hist=self.pos_hist[1:]
        self.pos_hist.append(temp_position)

        if len(self.time_hist)>=HIST_BUFFER:
            self.time_hist=self.time_hist[1:]
        self.time_hist.append(elapsedtime)


    @property
    def position(self):
         """Return last position."""
         #print (self.guessing_enabled)

         if len(self.pos_hist):
             return self.pos_hist[-1]
         else:
             return None

    #This function is not in use
    @property
    def position_guessed(self):
        """Get position based on history. Could allow for fancy filtering etc."""
        return geom.guessedPosition(self.pos_hist)

    def getLinkedLEDs(self):
        return self.linked_leds

    def addLinkedLED(self, led):
        self.reset()
        self.linked_leds.append(led)

    def removeLinkedLED(self, led):
        try:
            self.linked_leds.remove(led)
            self.reset()
        except ValueError:
            pass

    def getPositionX(self):
        """ Helper method to provide chatter with function reference for slot updates"""
        return None if self.position is None else self.position[0]

    def getPositionY(self):
        """ Helper method to provide chatter with function reference for slot updates"""
        return None if self.position is None else self.position[1]

    def getSpeed(self):
        """ Helper method to provide chatter with function reference for slot updates"""
        if len(self.speed_hist)>1:
            return self.speed_hist[-1]
        else:
            return None
        #return self.sp   #only returns the value without recalculating it

    def velocity(self, elapsedtime):
        """Return movement speed in pixel/s."""
        try:
            if len(self.pos_hist)>=2:
                if self.pos_hist[-1] is not None and self.pos_hist[-2] is not None:
                    #calculate speed
                    ds=geom.distance(self.pos_hist[-1], self.pos_hist[-2])
                    self.movdir=geom.angle(self.pos_hist[-2], self.pos_hist[-1])
                    dt= elapsedtime
                    self.sp=ds/dt
                #elif len(self.speed_hist>0):
                    # if the previous one was a valid value, this one will be too, if not, it will be None too
                 #   self.sp=self.speed_hist[-1]
                else:
                    self.sp=None
                    self.movdir=None
            else:
                self.sp = None
                self.movdir=None

        except TypeError:
            self.sp=None
            self.movdir=None
        finally:
            # works as a FIFO
            if len(self.speed_hist) >= HIST_BUFFER:
                self.speed_hist = self.speed_hist[1:]
            self.speed_hist.append(self.sp)
                # works as a FIFO
            if len(self.mov_dir_hist) >= HIST_BUFFER:
                self.mov_dir_hist = self.mov_dir_hist[1:]
            self.mov_dir_hist.append(self.movdir)

    def angularVelocity(self, elapsedtime):
        angvel=None
        if len(self.orientation_hist)>2:
            if self.orientation_hist[-1] is not None and self.orientation_hist[-2] is not None:
                angvel=(self.orientation_hist[-1]-self.orientation_hist[-2])/elapsedtime

        if len(self.ang_vel_hist) >= HIST_BUFFER:
            self.ang_vel_hist = self.ang_vel_hist[1:]
        self.ang_vel_hist.append(angvel)

    def getAngVel(self):
        if len(self.ang_vel_hist)>1:
            return self.ang_vel_hist[-1]
        else:
            return None

    def getOrientation(self):
        """ Helper method to provide chatter with function reference for slot updates"""
        if len(self.orientation_hist) > 1:
            return self.orientation_hist[-1]
        else:
            return None
    
    def getMovementDir(self):
        if len(self.mov_dir_hist) > 1:
            return self.mov_dir_hist[-1]
        else:
            return None

    def orientation(self):
        """
        Calculate orientation of the object.

        The function only calculate orientation for two markers.
        If there is only one, or more than two, it doesn't return a result.
        If there are exactly two markers, it calculates angle
         relative to normal of markers.

        This assumes the alignment of markers is constant.
        """
        # TODO: Calculate angle when having multiple markers
        headorientation = None
        try:
            #only calculating head orientation if there are at least two linked LED's
            if not self.tracked or self.linked_leds is None or len(self.linked_leds) != 2:
                return None

            marker_coords = []
            for marker in self.linked_leds:
                if len(marker.pos_hist) > 0 and marker.pos_hist[-1] is not None:
                    marker_coords.append(marker.pos_hist[-1])

            if len(marker_coords) == 2: #if both head direction values exist

                dx = (marker_coords[1][0] - marker_coords[0][0]) * 1.0  # x2-x1
                dy = (marker_coords[1][1] - marker_coords[0][1]) * 1.0  # y2-y1
                headorientation = int(math.fmod(math.degrees(math.atan2(dx, dy)) + 180, 360))  # math.atan2(x2-x1, y2-y1)

            ####################################################################################################################################
           # elif len(self.orientation_hist) > 0 and self.orientation_hist[-1] is not None:
           #     headorientation = self.orientation_hist[-1]
            #else:
               # print "one of the LED values are missing"


        except TypeError:
            headorientation = None

        finally:
            if len(self.orientation_hist)>=HIST_BUFFER:
                self.orientation_hist=self.orientation_hist[1:]
            self.orientation_hist.append(headorientation)
        return headorientation

    @property
    def linked_slots(self):
        """ Return list of slots that are linked to a pin. """
        # slots_to_update = []
        # for s in self.slots:
        #    if s.pin:
        #        slots_to_update.append(s)
        # return slots_to_update
        return [slot for slot in self.slots if slot.pin]

    def reset(self):
        #reset deletes the object's history
        self.pos_hist=[]
        self.orientation_hist=[]
        self.speed_hist=[]
        self.mov_dir_hist=[]
        self.ang_vel_hist=[]
        self.time_hist=[]

#generates a square wave that can be used to measure the output frame rate-->always uses D3
class fpsTestSignal:
    def __init__(self, pin):
        self.even_frame=True
        self.slot = Slot('fpstest', 'digital', self.flipstate, self)

    def attach_pin(self, pin):
        self.slot.attach_pin(pin)
    def deattach_pin(self):
        self.slot.detach_pin()

    def flipstate(self, state_idx):
        self.even_frame = not self.even_frame
        return self.even_frame


class RegionOfInterest:
    """ Region in image registered objects are tested against.
    If trackables are occupying or intersecting, trigger their specific
    callbacks.
    """
    visible = True
    color = None
    alpha = .4
    highlighted = False

    strict_prefs_dealt = False

    linked_objects = None  # aka slots?!

    normal_color = None
    active_color = None
    passive_color = None

    def __init__(self, shape_list=None, label=None, color=None, obj_list=None, magnetic_objects=None):
        self.label = label

        # Aesthetics
        self.update_color(color)
        self.set_passive_color()

        # slots linked to pins for physical output
        self.slots = []
        # reference to all objects spotter holds
        self.oois = obj_list
        # The slots for these objects are trying to automatically link pins
        if magnetic_objects is None:
            self.magnetic_objects = []
        else:
            self.magnetic_objects = magnetic_objects

        # if initialized with starting set of shapes
        self.shapes = []
        if shape_list:
            for shape in shape_list:
                self.add_shape(*shape)

    def update_state(self):
        self.highlighted = False
        self.deal_pin_prefs()

    def deal_pin_prefs(self):
        for mo in self.magnetic_objects:
            for s in self.slots:
                if s.ref == mo[0]:
                    s.pin_pref = mo[1]

    def update_slots(self, chatter):
        for slot in self.slots:
            if (slot.pin_pref is not None) and (slot.pin is None):
                pins = chatter.pins_for_slot(slot)
                for p in pins:
                    if p.id == slot.pin_pref:
                        slot.attach_pin(p)

    def update_color(self, color=None):
        """ Set color for region, used by all associated shapes. If no color
        give, will generate a random (most often ugly) on.
        """
        if not color:
            # Generating color
            self.normal_color = self.get_normal_color()
        else:
            self.normal_color = self.normalize_color(color)
        self.passive_color = self.scale_color(self.normal_color, 150)
        self.active_color = self.scale_color(self.normal_color, 255)

    @property
    def linked_slots(self):
        """ Return list of slots that are linked to a pin. """
        slots_to_update = []
        for slot in self.slots:
            if slot.pin:
                slots_to_update.append(slot)
        return slots_to_update

    def move(self, dx, dy):
        """ Moves all shapes, aka the whole ROI, by delta pixels. """
        for shape in self.shapes:
            shape.move(dx, dy)

    def add_shape(self, shape_type, points, label):
        """ Adds a new shape. """
        shape = Shape(shape_type, points, label)
        self.shapes.append(shape)
        return shape

    def remove_shape(self, shape):
        """ Removes a shape. """
        try:
            self.shapes.remove(shape)
        except ValueError:
            print "Couldn't find shape for removal"

    def refresh_slot_list(self):
        """
        Gather all objects in list. Check done by name.
        """
        # TODO: By label is risky, could lead to collisions
        # if self.oois and len(self.slots) < len(self.oois):
        for o in self.oois:
            for slot in self.slots:
                if slot.ref is o:
                    break
            else:
                self.link_object(o)

        for slot in self.slots:
            if not slot.ref in self.oois:
                self.unlink_object(slot.ref)

    def link_object(self, obj):
        print "Linked Object", obj.label, "to", self
        if obj in self.oois:
            self.slots.append(Slot(label=obj.label, slot_type='digital', state=self.test_collision,
                                   state_idx=obj, ref=obj))

    def unlink_object(self, obj):
        for slot in self.slots:
            if slot.ref is obj:
                self.slots.remove(slot)
                print "Removed object", obj.label, "from slot list of", self.label

    def test_collision(self, obj):
        return self.check_shape_collision(obj.position)

    def check_shape_collision(self, point1, point2=None):
        """ Test if a line between start and end would somewhere collide with
        any shapes of this ROI. Simple AND values in the collision detection
        array on the line.
        """
        # TODO: Only checks of the point is within the bounding box of shapes?
        if point1 is not None:
            collision = False
            for s in self.shapes:
                if s.active and s.collision_check(point1):
                    self.highlighted = True
                    collision = True
                    break

            # no collisions detected for this region
            self.toggle_highlight()
            return collision
        else:
            return None

    def toggle_highlight(self):
        """ Toggle color to active set if region is highlighted by collision. """
        if self.highlighted:
            if self.normal_color != self.active_color:
                self.set_active_color()
        else:
            if self.normal_color != self.passive_color:
                self.set_passive_color()

    def set_active_color(self):
        self.color = self.active_color
        self.alpha = 0.8
        self.normal_color = self.normalize_color(self.color)

    def set_passive_color(self):
        self.color = self.passive_color
        self.alpha = 0.4
        self.normal_color = self.normalize_color(self.color)

    def get_normal_color(self):
        c1 = random.random()
        c2 = random.uniform(0, 1.0 - c1)
        c3 = 1.0 - c1 - c2
        values = random.sample([c1, c2, c3], 3)
        return values[0], values[1], values[2], self.alpha

    @staticmethod
    def scale_color(color, max_val):
        if len(color) == 3:
            return int(color[0] * max_val), int(color[1] * max_val), int(color[2] * max_val)
        elif len(color) == 4:
            return int(color[0] * max_val), int(color[1] * max_val), int(color[2] * max_val), int(color[3] * max_val)

    @staticmethod
    def normalize_color(color):
        if len(color) == 3:
            return color[0] / 255., color[1] / 255., color[2] / 255.
        elif len(color) == 4:
            return color[0] / 255., color[1] / 255., color[2] / 255., color[3] / 255.


class BlindSpot:
    def __init__(self, mask_list=None, label=None):
        self.label=label
        self.active=True
        # if initialized with starting set of shapes
        self.masks = []
        if mask_list:
            for m in mask_list:
                self.add_mask(*m)

    def move(self, dx, dy):
        """ Moves all masks, aka the whole blindspot, by delta pixels. """
        for mask in self.masks:
            mask.move(dx, dy)

    def add_mask(self, shape_type, points, label):
        """ Adds a new shape. """
        mask = Mask(shape_type, points, label)
        self.masks.append(mask)
        return mask

    def remove_mask(self, mask):
        """ Removes a mask. """
        try:
            self.masks.remove(mask)
        except ValueError:
            print "Couldn't find mask for removal"

