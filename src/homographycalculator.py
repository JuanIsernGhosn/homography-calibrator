import numpy as np
import cv2

class HomographyCalculator:

    def __init__(self, filename, img):
        self.image = Observable(Image(filename, img))
        self.left_up_corner_px = (0, 0)
        self.right_up_corner_px = (0, 0)
        self.left_down_corner_px = (0, 0)
        self.right_down_corner_px = (0, 0)
        self.left_up_corner_coor = (0, 0)
        self.right_up_corner_coor = (0, 0)
        self.left_down_corner_coor = (0, 0)
        self.right_down_corner_coor = (0, 0)
        self.h = np.zeros((3,3))

    def calculate_h(self):
        px = [self.left_up_corner_px, self.right_up_corner_px, self.left_down_corner_px, self.right_down_corner_px]
        coor = [self.left_up_corner_coor, self.right_up_corner_coor, self.left_down_corner_coor, self.right_down_corner_coor]
        self.h = cv2.findHomography(px, coor)

    def change_image(self, filename, img):
        self.image.set(Image(filename, img))

    def get_real_mousse_loc(self,point):
        x = point[0]*self.image.get().width
        y = point[1]*self.image.get().height
        return (round(x),round(y))


class Observable:

    def __init__(self, data):
        self.data = data
        self.callbacks = {}

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callbacks[func]

    def _doAllCallbacks(self):
        for func in self.callbacks:
            func(self.data)

    def set(self, data):
        self.data = data
        self._doAllCallbacks()

    def get(self):
        return self.data

    def unset(self):
        self.data = None

class Image:
    def __init__(self, filename, img):
        self.filename = filename
        self.img = img
        self.width = None if img is None else img.size[0]
        self.height = None if img is None else img.size[1]