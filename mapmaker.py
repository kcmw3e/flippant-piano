################################################################################
#
#   mapmaker.py
#   Code by: Casey Walker
#
################################################################################

import pyglet
import app
import shapes
import layer
import copy
import random
from pyglet.window import key
import gui
import cursor
import voronoi
import map_obj

class Map_maker(app.App):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.setup()

    def setup(self):
        self.map_obj_types = [
                            ["Tree", "Oak"],
                            ["Tree", "Spruce"],
                            ["Mountain", "Snowy"],
                            ["Hill"],
                            ["Lake"],
                            ["House"]
                             ]

        self.voronoi_object_sets = [
                            [ ["Tree", "Oak"], ["Mountain"] ],
                            [ ["Tree", "Spruce"], ["Mountain", "Snowy"] ],
                            [ ["Tree", "Oak"], ["House"] ],
                            [ ["Tree", "Spruce"], ["House"] ],
                            [ ["Hill"] ],
                                   ]

        self.scale = 1

        self.oak_tree_leaf_color =  [45, 112, 3]
        self.oak_tree_trunk_color = [112, 52, 3]
        self.oak_tree_leaves = 1
        self.oak_tree_width = 10
        self.oak_tree_height = 20

        self.spruce_tree_leaf_color =  [29, 84, 24]
        self.spruce_tree_trunk_color = [94, 60,  2]
        self.spruce_tree_leaves = 3
        self.spruce_tree_width = 10
        self.spruce_tree_height = 20

        self.mountain_rock_color = [112, 112, 112]
        self.mountain_snow_color = [255, 255, 255]
        self.mountain_width = 30
        self.mountain_height = 40

        self.hill_color = [15, 112, 26]
        self.hill_width = 5
        self.hill_height = 5

        self.lake_water_color = [0, 0, 180]

        self.house_wall_color = [201, 112, 66]
        self.house_door_color = [89, 68, 40]
        self.house_roof_color = [77, 72, 65]
        self.house_width = 10
        self.house_height = 10

        self.layer_setup()
        self.clock_setup()
        self.cursor_setup()
        self.gui_setup()

    def layer_setup(self):
        self.layer_percent = 0.9
        self.layer_width = self.width
        self.layer_height = self.height * self.layer_percent
        self.layer_color = [240, 194, 112]
        self.layer_color = [136, 189,  23]
        self.layer = layer.Layer(self.layer_width, self.layer_height,
                                 self.layer_color)

    def cursor_setup(self):
        self.cursor = cursor.Cursor(None, None)

    def gui_setup(self):
        #the functions for each button to call when pressed
        self.gui_button_functions = [self.change_cursor_type, 
                                     self.change_cursor_type,
                                     self.change_cursor_type,
                                     self.change_cursor_type,
                                     self.change_cursor_type,
                                     self.change_cursor_type,
                                     self.generate_random_map,
                                     self.clear_map]
        #the arguments to be called in the functions ^^above^^
        self.gui_button_args = [ 
            [ self.add_map_obj, 
              (self.cursor.get_pos, "Tree", "Oak", True),
              "Map_obj" ],

            [ self.add_map_obj,
              (self.cursor.get_pos, "Tree", "Spruce", True),
              "Map_obj" ],

            [ self.add_map_obj,
              (self.cursor.get_pos, "Mountain", "Snowy", True),
              "Map_obj" ],

            [ self.add_map_obj,
              (self.cursor.get_pos, "Hill", None, True),
              "Map_obj" ],

            [ self.add_map_obj,
              (self.cursor.get_pos, "Lake", None, True),
              "Map_obj" ],

            [ self.add_map_obj,
              (self.cursor.get_pos, "House", None, True),
              "Map_obj"],

            [ ],

            [ ]
        ]
        self.gui_button_labels = ["Oak Tree",
                                  "Spruce Tree",
                                  "Mountain",
                                  "Hill",
                                  "Lake",
                                  "House",
                                  "Random Map",
                                  "Clear Map"]
        self.gui_button_label_colors = [ [255, 255, 255, 255],
                                         [255, 255, 255, 255],
                                         [255, 255, 255, 255],
                                         [255, 255, 255, 255],
                                         [255, 255, 255, 255],
                                         [255, 255, 255, 255],
                                         [255, 255, 255, 255],
                                         [255, 255, 255, 255] ]

        self.gui_button_colors = [       [50, 112, 255],
                                         [50, 112, 255],
                                         [50, 112, 255],
                                         [50, 112, 255],
                                         [50, 112, 255],
                                         [50, 112, 255],
                                         [50, 112, 255],
                                         [70,  70,  70] ]

        self.gui_button_hover_colors = [ [92, 39, 211],
                                         [92, 39, 211],
                                         [92, 39, 211],
                                         [92, 39, 211],
                                         [92, 39, 211],
                                         [92, 39, 211],
                                         [214, 73, 200],
                                         [245, 66, 72] ]

        self.gui_width = self.width
        self.gui_height = self.height - self.layer_height
        self.gui_color = [220, 112, 50]
        self.gui_pos = (self.width / 2, self.height - self.gui_height / 2)
        self.gui = gui.GUI(self.gui_pos, self.gui_width, self.gui_height,
                           self.gui_color, self.gui_button_functions,
                           self.gui_button_args, self.gui_button_labels,
                           self.gui_button_colors, self.gui_button_label_colors,
                           self.gui_button_hover_colors)

    def clock_setup(self):
        self.clock = pyglet.clock.get_default()
        self.clock.schedule(self.clock_ticked)

    def voronoi_setup(self):
        #Be aware that if the seed number is too large, it may take
        #a very (very) long time to solve the voronoi diagram.
        #Also note that if too many seeds exist with too high padding,
        #a diagram may fail to be created
        self.voronoi_seeds_number = 10
        self.voronoi_seeds_padding = 80
        self.voronoi = voronoi.Voronoi(self.width, self.layer_height,
                                       self.voronoi_seeds_number, 
                                       self.voronoi_seeds_padding)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.gui.show_help_menu(True)

    def on_key_release(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.gui.show_help_menu(False)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        super().on_mouse_scroll(x, y, scroll_x, scroll_y)
        self.cursor.pos = (x, y)
        self.scale += scroll_y

    def on_mouse_press(self, x, y, buttons, modifiers):
        super().on_mouse_press(x, y, buttons, modifiers)
        self.cursor() #call the function that cursor holds
        if self.gui.hovered:
            #to tell gui it should draw itself as hovered
            self.gui.cursor_hovered(self.cursor_pos, clicked = True)

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)
        self.cursor.pos = (x, y)
        if self.gui.hovered:
            #to tell gui it should draw itself as hovered
            self.gui.cursor_hovered(self.cursor.pos)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        super().on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        self.cursor.pos = (x, y)
        self.cursor() #call the function that cursor holds

    def on_draw(self):
        super().on_draw()
        self.layer.draw()
        self.gui.draw()
        self.cursor.draw()

    def on_resize(self, width, height):
        super().on_resize(width, height)

    #from cursor is to know if pos is given as a function that returns a pos
    #or if pos is a tuple containing (x, y)
    def add_map_obj(self, pos, obj_type, obj_subtype = None,
                    from_cursor = False):
        obj = self.make_map_obj(pos, obj_type, obj_subtype,
                                from_cursor = from_cursor)
        self.layer.add_if_not_intersecting(obj)

    def make_map_obj(self, pos, obj_type, obj_subtype = None,
                     alpha = False, alpha_value = None, from_cursor = False):
        if from_cursor:
            pos = pos()
        if obj_type == "Tree":
            if obj_subtype == "Oak":
                leaf_color = copy.copy(self.oak_tree_leaf_color)
                trunk_color = copy.copy(self.oak_tree_trunk_color)
                leafs = self.oak_tree_leaves
                width = self.oak_tree_width * self.scale
                height = self.oak_tree_height * self.scale
            elif obj_subtype == "Spruce":
                leaf_color = copy.copy(self.spruce_tree_leaf_color)
                trunk_color = copy.copy(self.spruce_tree_trunk_color)
                leafs = self.spruce_tree_leaves
                width = self.spruce_tree_width * self.scale
                height = self.spruce_tree_height * self.scale
            if alpha:
                leaf_color.append(alpha_value)
                trunk_color.append(alpha_value)
            obj = map_obj.Tree(pos, width, height, 
                               leaf_color, trunk_color, leafs)
        elif obj_type == "Mountain":
            rock_color = copy.copy(self.mountain_rock_color)
            snow_color = copy.copy(self.mountain_snow_color)
            width = self.mountain_width * self.scale
            height = self.mountain_height * self.scale
            snow = False
            if obj_subtype == "Snowy":
                snow = True
            if alpha:
                rock_color.append(alpha_value)
                snow_color.append(alpha_value)
            obj = map_obj.Mountain(pos, width, height,
                                   rock_color, snow, snow_color)
        elif obj_type == "Hill":
            hill_color = copy.copy(self.hill_color)
            width = self.hill_width * self.scale
            height = self.hill_height * self.scale
            if alpha:
                hill_color.append(alpha_value)
            obj = map_obj.Hill(pos, width, height, hill_color)
        elif obj_type == "Lake":
            lake_color = copy.copy(self.lake_water_color)
            if alpha:
                lake_color.append(alpha_value)
            obj = map_obj.Lake(pos, 30, 30, lake_color)
        elif obj_type == "House":
            wall_color = copy.copy(self.house_wall_color)
            door_color = copy.copy(self.house_door_color)
            roof_color = copy.copy(self.house_roof_color)
            width = self.house_width * self.scale
            height = self.house_height * self.scale
            if alpha:
                wall_color.append(alpha_value)
                door_color.append(alpha_value)
                roof_color.append(alpha_value)
            obj = map_obj.House(pos, width, height, wall_color, door_color, roof_color)
        return obj

    def generate_random_map(self):
        self.voronoi_setup()
        self.voronoi.solve()
        self.voronoi_batch = pyglet.graphics.Batch()
        self.populate_voronoi()

    def populate_voronoi(self):
        self.voronoi_polygons = dict()
        for seed in self.voronoi.seeds:
            polygon = seed.get_polygon()
            seed.polygon = polygon
            seed.map_obj_set = random.choice(self.voronoi_object_sets)
            self.populate_seed(seed)

    def populate_seed(self, seed):
        (min_x, max_x, min_y, max_y) = seed.polygon.get_maxs_and_mins()
        for _ in range(300):
            obj_type = random.choice(seed.map_obj_set)
            x = random.randrange(int(min_x), int(max_x) + 1) #+1 in case euqal
            y = random.randrange(int(min_y), int(max_y) + 1) #+1 in case euqal
            pos = (x, y)
            if seed.polygon.contains_point(pos):
                self.add_map_obj(pos, *obj_type)

    def clear_map(self):
        self.layer_setup() #layer setup will just re-make the layer and regions

    def toggle_cursor_visibility(self, set_to = None):
        self.cursor.toggle_visibility(set_to)
        self.set_mouse_visible(self.cursor.visibility)

    def clock_ticked(self, dt):
        self.update_cursor()
        if self.gui.hovered:
            self.gui.cursor_hovered(self.cursor.pos)

    def update_cursor(self):
        if self.gui.has_cursor(self.cursor.pos):
            self.toggle_cursor_visibility(True)
            self.cursor.toggle_img_visibility(False)
            self.gui.hovered = True
        elif self.cursor.type != None:
            self.cursor.toggle_img_visibility(True)
            self.toggle_cursor_visibility(False)
            self.gui.hovered = False
        if self.cursor.type == "Map_obj":
            self.cursor.img = self.make_map_obj(*self.cursor.args[:-1], 
                                                alpha = True, alpha_value = 112,
                                                from_cursor = True)

    def change_cursor_type(self, function, args, cursor_type):
        self.cursor.function = function
        self.cursor.args = args
        self.cursor.type = cursor_type

map_maker = Map_maker(1280, 720)
map_maker.set_caption("Map Maker")
pyglet.app.run()