import numpy as np
from src.Model.image import Image
from src.Model.observable import Observable
import cv2

class HomographyCalculator:

    def __init__(self, filename=None, img=None):
        self.image = Observable(Image(filename, img))
        self.px = Observable(np.zeros((4,2), dtype=np.float32))
        self.px_bird = Observable(np.zeros((4, 2), dtype=np.float32))
        self.coord = Observable(np.zeros((4,2), dtype=np.float32))
        self.h = Observable(np.zeros((3,3), dtype=np.float32))

    def calculate_h(self):
        h, m = cv2.findHomography(self.px.get(), self.coord.get(), cv2.RANSAC)
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

    def update_coords(self, coords, index):
        coord = self.coord.data
        coord[int(index)] = coords
        self.coord.set(coord)

    def update_point_coords(self, point, index):
        px_bird = self.px_bird.data
        px_bird[int(index)] = point
        self.px_bird.set(px_bird)
