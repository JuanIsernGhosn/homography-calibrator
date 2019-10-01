import numpy as np
import cv2

class HomographyCalculator:

    def __init__(self, filename, img):
        self.image = Observable(Image(filename, img))
        self.px = Observable(np.zeros((4,2), dtype=np.float32))
        self.coord = np.zeros((4,2), dtype=np.float32)
        self.h = Observable(np.zeros((3,3), dtype=np.float32))

    def calculate_h(self, coord):
        self.coord=coord
        h, m = cv2.findHomography(self.px.get(), self.coord, cv2.RANSAC)
        h = np.zeros((3,3), dtype=np.float32) if h is None else h
        self.h.set(h)

    def change_image(self, filename, img):
        self.image.set(Image(filename, img))

    def get_real_mousse_loc(self,point):
        x = point[0]*self.image.get().width
        y = point[1]*self.image.get().height
        return (x,y)

    def update_point_loc(self, point, index):
        px = self.px.data
        px[int(index)] = self.get_real_mousse_loc(point)
        self.px.set(px)

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