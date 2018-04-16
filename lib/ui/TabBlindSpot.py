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
    region = None
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
        self.region = region_ref
        print self.region

        assert 'spotter' in kwargs
        self.spotter = kwargs['spotter']

        # if label is None:
        #     self.label = self.region.label
        # else:
        #     self.label = label
        #     self.region.label = label
        #
        # # Fill tree/list with all available shapes
        # for s in self.region.shapes:
        #     shape_item = QtGui.QTreeWidgetItem([s.label])
        #     shape_item.shape = s
        #     shape_item.setCheckState(0, QtCore.Qt.Checked)
        #     shape_item.setFlags(shape_item.flags() | QtCore.Qt.ItemIsEditable)
        #     self.tree_region_shapes.addTopLevelItem(shape_item)
        #
        # # List of items in the table to compare when updated. Ugly solution.
        # self.slots_items = []
        #
        # self.connect(self.btn_add_rect, QtCore.SIGNAL('toggled(bool)'), self.rect_clicked)
        # self.connect(self.btn_add_line, QtCore.SIGNAL('toggled(bool)'), self.line_clicked)
        # self.connect(self.btn_add_circle, QtCore.SIGNAL('toggled(bool)'), self.circle_clicked)
        #
        # self.connect(self.btn_remove_shape, QtCore.SIGNAL('clicked()'), self.remove_shape)
        # #self.connect(self.btn_lock_table, QtCore.SIGNAL('toggled(bool)'), self.lock_slot_table)
        #
        # # coordinate spin box update signals
        # self.connect(self.spin_shape_x, QtCore.SIGNAL('valueChanged(int)'), self.update_shape_position)
        # self.connect(self.spin_shape_y, QtCore.SIGNAL('valueChanged(int)'), self.update_shape_position)
        #
        # # if a checkbox or spinbox on a shape in the list is changed
        # self.spin_shape = None
        # self.connect(self.tree_region_shapes, QtCore.SIGNAL('itemChanged(QTreeWidgetItem *, int)'),
        #              self.shape_item_changed)
        # self.connect(self.tree_region_shapes, QtCore.SIGNAL('itemSelectionChanged()'), self.update_spin_boxes)
        #
        # if self.region.active_color is not None:
        #     ss_string = "background-color: rgba({0[0]}, {0[1]}, {0[2]})".format(self.region.active_color)
        #     self.lbl_color.setStyleSheet(ss_string)
        # self.lbl_color.mouseReleaseEvent = self.change_color
    #
    #     self.update()
    #
    # def update(self):
    #     self.refresh_shape_list()
    #     self.refresh_slot_table()
    #     self.update_spin_boxes()
    #
    # def update_spin_boxes(self):
    #     tree_item = self.tree_region_shapes.selectedItems()
    #     if tree_item:
    #         tree_item = tree_item[0]
    #         # update spin boxes if the coordinates differ between shape and spin box
    #         if not self.spin_shape_x.value() == tree_item.shape.points[0][0]:
    #             self.spin_shape_x.setValue(tree_item.shape.points[0][0])
    #         if not self.spin_shape_y.value() == tree_item.shape.points[0][1]:
    #             self.spin_shape_y.setValue(tree_item.shape.points[0][1])
    #
    # def accept_selection(self, state):
    #     """ Called by the 'Add' button toggle to accept input for new shapes """
    #     self.event_add_selection = state
    #
    # def rect_clicked(self, state):
    #     self.accept_selection(state)
    #     self.spotter.active_shape_type='rectangle'
    #     self.btn_add_rect.setChecked(True)
    #     self.btn_add_line.setChecked(False)
    #     self.btn_add_circle.setChecked(False)
    #
    # def line_clicked(self, state):
    #     self.accept_selection(state)
    #     self.spotter.active_shape_type = 'line'
    #     self.btn_add_line.setChecked(True)
    #     self.btn_add_rect.setChecked(False)
    #     self.btn_add_circle.setChecked(False)
    #
    # def circle_clicked(self, state):
    #     self.accept_selection(state)
    #     self.spotter.active_shape_type = 'circle'
    #     self.btn_add_circle.setChecked(True)
    #     self.btn_add_rect.setChecked(False)
    #     self.btn_add_line.setChecked(False)
    #
    #
    # def process_event(self, event_type, event):
    #     """ Handle mouse interactions, mainly to draw and move shapes """
    #     modifiers = QtGui.QApplication.keyboardModifiers()
    #
    #     if event_type == "mousePress":
    #         self.button_start = int(event.buttons())
    #         self.coord_start = [event.x(), event.y()]
    #         self.coord_last = self.coord_start
    #     elif event_type == "mouseDrag":
    #         if int(event.buttons()) == QtCore.Qt.MiddleButton:
    #             dx = event.x() - self.coord_last[0]
    #             dy = event.y() - self.coord_last[1]
    #             self.coord_last = [event.x(), event.y()]
    #             if modifiers == QtCore.Qt.ShiftModifier:
    #                 self.move_region(dx, dy)
    #             else:
    #                 self.move_shape(dx, dy)
    #
    #             self.spin_shape = None
    #             self.update_spin_boxes()
    #     elif event_type == "mouseRelease":
    #         # Beware button vs. buttons. buttons() does not hold the button triggering
    #         # the event. button() does for release, but not for move events.
    #         button = int(event.button())
    #         if not button == self.button_start:
    #             # user clicked different button than initially, to cancel
    #             # selection I presume
    #             self.coord_end = None
    #             self.coord_start = None
    #             self.button_start = None
    #             return
    #
    #         if button == QtCore.Qt.LeftButton and self.event_add_selection:
    #             # Finalize region selection
    #             self.coord_end = [event.x(), event.y()]
    #
    #             shape_type = self.spotter.active_shape_type
    #             # if modifiers == QtCore.Qt.NoModifier:
    #             #     shape_type = 'rectangle'
    #             # elif modifiers == QtCore.Qt.ShiftModifier:
    #             #     shape_type = 'circle'
    #             # elif modifiers == QtCore.Qt.ControlModifier:
    #             #     shape_type = 'line'
    #
    #             shape_points = [self.coord_start, self.coord_end]
    #             if shape_type and shape_points:
    #                 self.add_shape(shape_type, shape_points)
    #     else:
    #         print 'Event not understood. Hulk sad and confused.'
    #
    # def move_region(self, dx, dy):
    #     self.region.move(dx, dy)
    #
    # def update_region(self):
    #     if self.label is None:
    #         print "Empty object tab! This should not have happened!"
    #         return

# ###############################################################################
# ## SHAPE LIST
# ###############################################################################
#
#     def refresh_shape_list(self):
#         # If nothing selected, select the first item in the list
#         n_items = self.tree_region_shapes.topLevelItemCount()
#         if n_items and not self.tree_region_shapes.currentItem():
#             self.tree_region_shapes.setCurrentItem(self.tree_region_shapes.topLevelItem(0))
#
#     def add_shape(self, shape_type, shape_points):  # , shape_label
#         """
#         Add a new geometric shape to the region. First, create a new
#         item widget. Add it to the region object via its add_shape function
#         which will take care of adding it to the list etc. Then add the item
#         to the tree widget. Last uncheck the "Add" button.
#         """
#         shape_item = QtGui.QTreeWidgetItem([shape_type])
#         shape_item.shape = self.region.add_shape(shape_type, shape_points, shape_type)
#         shape_item.setCheckState(0, QtCore.Qt.Checked)
#         self.tree_region_shapes.addTopLevelItem(shape_item)
#         self.tree_region_shapes.setCurrentItem(shape_item)
#         shape_item.setFlags(shape_item.flags() | QtCore.Qt.ItemIsEditable)
#         self.btn_add_rect.setChecked(False)
#
#     def remove_shape(self):
#         """ Remove a shape from the list defining a ROI """
#         if not self.tree_region_shapes.currentItem():
#             return
#         selected_item = self.tree_region_shapes.currentItem()
#         index = self.tree_region_shapes.indexOfTopLevelItem(selected_item)
#         if selected_item:
#             self.region.remove_shape(selected_item.shape)
#             self.tree_region_shapes.takeTopLevelItem(index)
#
#     def update_shape_position(self):
#         """
#         Update position of the shape if the values in the spin boxes,
#         representing the top right corner of the shape, is changed. Requires
#         checking if the spin box update is caused by just switching to a
#         different shape in the shape tree list!
#         """
#         if not self.tree_region_shapes.currentItem():
#             return
#
#         if self.tree_region_shapes.currentItem().shape == self.spin_shape:
#             # find the shape in the shape list of the RegionOfInterest
#             idx = self.region.shapes.index(self.tree_region_shapes.currentItem().shape)
#             dx = self.spin_shape_x.value() - self.region.shapes[idx].points[0][0]
#             dy = self.spin_shape_y.value() - self.region.shapes[idx].points[0][1]
#             self.move_shape(dx, dy)
#         else:
#             self.spin_shape = self.tree_region_shapes.currentItem().shape
#             return
#
#     def move_shape(self, dx, dy):
#         """
#         Update position of geometric shape by offsetting all points of shape
#         by delta coming from change of the spin boxes or dragging the mouse
#         while middle clicking
#         """
#         if not self.tree_region_shapes.currentItem():
#             return
#
#         if self.tree_region_shapes.currentItem().shape == self.spin_shape:
#             # find the shape in the shape list of the RegionOfInterest
#             idx = self.region.shapes.index(self.tree_region_shapes.currentItem().shape)
#             self.region.shapes[idx].move(dx, dy)
#         else:
#             self.spin_shape = self.tree_region_shapes.currentItem().shape
#             return
#
#     @staticmethod
#     def shape_item_changed(item, column):
#         """
#         Activate/inactive shapes. If not active, will not be included in
#         collision detection and will not be drawn/will be drawn in a distinct
#         way (i.e. only outline or greyed out?)
#         """
#         if item.checkState(column):
#             item.shape.active = True
#         else:
#             item.shape.active = False
#         item.shape.label = item.text(0)
#
