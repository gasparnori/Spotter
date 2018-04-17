# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 14:19:24 2013
@author: <Ronny Eichler> ronny.eichler@gmail.com


"""
import logging

from PyQt4 import QtGui, QtCore
from tab_blindspotUi import Ui_tab_regions
import lib.geometry as geom


class Tab(QtGui.QWidget, Ui_tab_regions):

    label = None
    blindspot = None
    accept_events = True
    event_add_selection = False
    tab_type = "blind spot"
    active_shape_type="rect"        #whichever shape type was chosen

    # mouse event handling
    start_coords = None
    coord_start = None
    coord_end = None
    coord_last = None
    button_start = None

    def __init__(self, region_ref, label=None, *args, **kwargs):
        #super(QtGui.QWidget, self).__init__(parent)
        QtGui.QWidget.__init__(self)
        self.log = logging.getLogger(__name__)
        self.setupUi(self)
        self.blindspot = region_ref
        #print self.region

        assert 'spotter' in kwargs
        self.spotter = kwargs['spotter']

        if label is None:
             self.label = self.blindspot.label
        else:
            self.label = label
            self.blindspot.label = label
        #
        # # Fill tree/list with all available shapes
        for s in self.blindspot.masks:
             shape_item = QtGui.QTreeWidgetItem([s.label])
             shape_item.shape = s
             shape_item.setCheckState(0, QtCore.Qt.Checked)
             shape_item.setFlags(shape_item.flags() | QtCore.Qt.ItemIsEditable)
             self.tree_blindspot_shapes.addTopLevelItem(shape_item)

        self.connect(self.btn_add, QtCore.SIGNAL('toggled(bool)'), self.blindspot_add)
        self.connect(self.radioCircle, QtCore.SIGNAL('toggled(bool)'), self.circle_shape)
        self.connect(self.radioLine, QtCore.SIGNAL('toggled(bool)'), self.line_shape)
        self.connect(self.radioRect, QtCore.SIGNAL('toggled(bool)'), self.rect_shape)
        self.connect(self.btn_remove_shape, QtCore.SIGNAL('clicked()'), self.remove_mask)
        # #self.connect(self.btn_lock_table, QtCore.SIGNAL('toggled(bool)'), self.lock_slot_table)
        #
        # # coordinate spin box update signals
        self.connect(self.spin_X, QtCore.SIGNAL('valueChanged(int)'), self.update_shape_position)
        self.connect(self.spin_Y, QtCore.SIGNAL('valueChanged(int)'), self.update_shape_position)
        #
        # # if a checkbox or spinbox on a shape in the list is changed
        self.spin_shape = None
        self.connect(self.tree_blindspot_shapes, QtCore.SIGNAL('itemChanged(QTreeWidgetItem *, int)'),
                     self.shape_item_changed)
        self.update()
    #
    def update(self):
         self.refresh_shape_list()

    def circle_shape(self, state):
        if state:
            self.active_shape_type='circle'
    def line_shape(self, state):
        if state:
            self.active_shape_type='line'
    def rect_shape(self, state):
        if state:
            self.active_shape_type='rect'
    def blindspot_add(self, state):
        """ Called by the 'Add' button toggle to accept input for new shapes """
        self.spotter.active_shape_type = self.active_shape_type
        self.event_add_selection = state
        print self.accept_events

    def process_event(self, event_type, event):
        """ Handle mouse interactions, mainly to draw and move shapes """
       # modifiers = QtGui.QApplication.keyboardModifiers()
        print "entered function"
        if event_type == "mousePress":
            self.button_start = int(event.buttons())
            self.coord_start = [event.x(), event.y()]
            self.coord_last = self.coord_start
        elif event_type == "mouseDrag":
            if int(event.buttons()) == QtCore.Qt.MiddleButton:
                dx = event.x() - self.coord_last[0]
                dy = event.y() - self.coord_last[1]
                self.coord_last = [event.x(), event.y()]
        elif event_type == "mouseRelease":
            # Beware button vs. buttons. buttons() does not hold the button triggering
            # the event. button() does for release, but not for move events.
            button = int(event.button())
            if not button == self.button_start:
                # user clicked different button than initially, to cancel
                # selection I presume
                self.coord_end = None
                self.coord_start = None
                self.button_start = None
                return

            if button == QtCore.Qt.LeftButton and self.event_add_selection:
                # Finalize region selection
                self.coord_end = [event.x(), event.y()]

                #shape_type = self.spotter.active_shape_type
                shape_points = [self.coord_start, self.coord_end]
                if self.shape_type and shape_points:
                    self.add_mask(self.shape_type, shape_points)
        else:
            print 'Event not understood. Hulk sad and confused.'

    def move_region(self, dx, dy):
        self.blindspot.move(dx, dy)

    def update_region(self):
        if self.label is None:
            print "Empty object tab! This should not have happened!"
            return

# ###############################################################################
# ## SHAPE LIST
# ###############################################################################

    def refresh_shape_list(self):
        # If nothing selected, select the first item in the list
        n_items = self.tree_blindspot_shapes.topLevelItemCount()
        if n_items and not self.tree_blindspot_shapes.currentItem():
            self.tree_blindspot_shapes.setCurrentItem(self.tree_blindspot_shapes.topLevelItem(0))

    def add_mask(self, shape_type, shape_points):  # , shape_label
        """
        Add a new geometric shape to the region. First, create a new
        item widget. Add it to the region object via its add_shape function
        which will take care of adding it to the list etc. Then add the item
        to the tree widget. Last uncheck the "Add" button.
        """
        shape_item = QtGui.QTreeWidgetItem([shape_type])
        shape_item.shape = self.blindspot.add_mask(shape_type, shape_points, shape_type)
        print shape_item.shape
        shape_item.setCheckState(0, QtCore.Qt.Checked)
        self.tree_blindspot_shapes.addTopLevelItem(shape_item)
        self.tree_blindspot_shapes.setCurrentItem(shape_item)
        shape_item.setFlags(shape_item.flags() | QtCore.Qt.ItemIsEditable)
        self.btn_add_rect.setChecked(False)
        self.btn_add_line.setChecked(False)
        self.btn_add_circle.setChecked(False)

    def remove_mask(self):
        """ Remove a shape from the list defining a ROI """
        if not self.tree_blindspot_shapes.currentItem():
            return
        selected_item = self.tree_blindspot_shapes.currentItem()
        index = self.tree_blindspot_shapes.indexOfTopLevelItem(selected_item)
        if selected_item:
            self.blindspot.remove_shape(selected_item.shape)
            self.tree_blindspot_shapes.takeTopLevelItem(index)
#
    def update_shape_position(self):
        """
        Update position of the shape if the values in the spin boxes,
        representing the top right corner of the shape, is changed. Requires
        checking if the spin box update is caused by just switching to a
        different shape in the shape tree list!
        """
        if not self.tree_blindspot_shapes.currentItem():
            return

        if self.tree_blindspot_shapes.currentItem().shape == self.spin_shape:
            # find the shape in the shape list of the RegionOfInterest
            idx = self.blindspot.masks.index(self.tree_blindspot_shapes.currentItem().shape)
            dx = self.spin_X.value() - self.blindspot.masks[idx].points[0][0]
            dy = self.spin_Y.value() - self.blindspot.masks[idx].points[0][1]
            self.move_shape(dx, dy)
        else:
            self.spin_shape = self.tree_blindspot_shapes.currentItem().shape
            return

    def move_shape(self, dx, dy):
        """
        Update position of geometric shape by offsetting all points of shape
        by delta coming from change of the spin boxes or dragging the mouse
        while middle clicking
        """
        if not self.tree_blindspot_shapes.currentItem():
            return

        if self.tree_blindspot_shapes.currentItem().shape == self.spin_shape:
            # find the shape in the shape list of the RegionOfInterest
            idx = self.blindspot.masks.index(self.tree_blindspot_shapes.currentItem().shape)
            self.blindspot.masks[idx].move(dx, dy)
        else:
            self.spin_shape = self.tree_blindspot_shapes.currentItem().shape
            return

    @staticmethod
    def shape_item_changed(item, column):
        """
        Activate/inactive shapes. If not active, will not be included in
        collision detection and will not be drawn/will be drawn in a distinct
        way (i.e. only outline or greyed out?)
        """
        if item.checkState(column):
            item.shape.active = True
        else:
            item.shape.active = False
        item.shape.label = item.text(0)

#removes the Blindspot from tracker: works
    def closeEvent(self, QCloseEvent):
        self.spotter.tracker.remove_blindspot(self.blindspot)
