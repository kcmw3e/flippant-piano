
class Cursor(object):
    def __init__(self, default_function, default_args):
        self.pos = (0, 0)
        self.default_function = default_function
        self.default_args = default_args
        self.function = self.default_function
        self.args = self.default_args
        self.visibility = True
        self.img = None
        self.img_visibility = False
        self.type = None

    def __call__(self, default = False):
        if default:
            self.default_function(*self.default_args)
        elif self.function != None:
            self.function(*self.args)
    
    def toggle_visibility(self, set_to = None):
        if set_to != None:
            self.visibility = set_to
        else:
            self.visibility = not self.visibility
    
    def toggle_img_visibility(self, set_to = None):
        if set_to != None:
            self.img_visibility = set_to
        else:
            self.img_visibility = not self.img_visibility

    def get_pos(self):
        return self.pos

    def draw(self):
        if self.img_visibility:
            self.img.draw()