import numpy as np
import cv2

class HomographyCalculator:

    def __init__(self):
        self.image = Observable()
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

    def set_image(self):
        self.image.


class Observable:
    def __init__(self, initialValue=None):
        self.data = initialValue
        self.callbacks = {}

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callbacks[func]

    def _docallbacks(self):
        for func in self.callbacks:
            func(self.data)

    def set(self, data):
        self.data = data
        self._docallbacks()

    def get(self):
        return self.data

    def unset(self):
        self.data = None
