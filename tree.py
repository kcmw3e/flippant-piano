################################################################################
#
#   tree.py
#   Code by: Casey Walker
#
################################################################################

import math
import pyglet
import shapes
import component

class Tree(object):
    def __init__(self, pos, width, height, 
                 leaf_color, trunk_color,
                 number_of_leaves):
        self.pos = pos
        self.width = width
        self.height = height
        self.leaf_color = leaf_color
        self.trunk_color = trunk_color
        self.number_of_leaves = number_of_leaves
        self.components = list()
        self.make_leaves()
        self.components.extend(self.leaves)
        self.make_trunk()
        self.components.append(self.trunk)

    def make_leaves(self):
        self.leaves = list()
        leaf_height = self.height*.9 / (self.number_of_leaves)
        for i in range(self.number_of_leaves):
            offset = (0, self.height - leaf_height * (i + 1) / 2)
            t = shapes.Iso_triangle(self.pos, self.width, leaf_height * (i + 1), offset)
            l = component.Component(t, self.leaf_color, pyglet.gl.GL_POLYGON)
            self.leaves.append(l)

    def make_trunk(self):
        trunk_height = self.height *.1
        trunk_width = self.width / 3
        x = self.pos[0]
        y = self.pos[1] + trunk_height / 2
        r = shapes.Rect((x, y), trunk_width, trunk_height)
        self.trunk = component.Component(r, self.trunk_color, pyglet.gl.GL_POLYGON)

    def is_near(self, other):
        x_max = (self.width + other.width) * .5 #for padding of inaccuracy
        y_max = (self.height + other.height) * .5
        dx = abs(self.pos[0] - other.pos[0])
        dy = abs(self.pos[1] - other.pos[1])
        if dx <= x_max and dy <= y_max:
            return True
        else:
            return False

    def intersects(self, other):
        if self.is_near(other):
            for component in self.components:
                for other_component in other.components:
                    if component.intersects(other_component):
                        return True
            return False

    def is_near(self, other):
        if abs(self.pos[0] - other.pos[0]) <= max(self.width, other.width) and abs(self.pos[1] - other.pos[1]) <= max(self.height, other.height):
            return True
        else:
            return False

    def draw(self):
        for component in self.components:
            component.vertex_list.draw(component.draw_type)