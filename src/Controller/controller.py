from src.View.appgui import ApplicationGUI
from src.Model.homographycalculator import HomographyCalculator
from src.Model.JSON.modeldeserializer import CalculatorDeserializer
from tkinter import filedialog
from PIL import Image
from src.Model.JSON import jsonserializer
import itertools
import numpy as np

class Controller:
    def __init__(self, root):
        self.view = ApplicationGUI(root)
        self.view.menu1.entryconfigure('Open image', command=self.change_image_diag)
        self.view.menu1.entryconfigure('Load config. file', command=self.load_conf_file)
        self.view.menu1.entryconfigure('Save config. file', command=self.save_conf_file)
        self.view.button_homography.configure(command=self.calculate_homography)
        self.calculator = HomographyCalculator()
        self.calculator.image.addCallback(self.image_changed)
        self.calculator.px.addCallback(self.point_updated)
        self.calculator.h.addCallback(self.h_updated)
        self.calculator.coord.addCallback(self.coord_updated)
        self.view.panel_image.bind('<Motion>', self.change_mousse_loc)
        self.view.panel_image.bind('<Button-1>', self.update_point_loc)

    def load_conf_file(self):
        filename = filedialog.askopenfilename(initialdir=".",
                                              title="Open configuration file",
                                              filetypes= (("txt files","*.txt"),
                                                           ("all files","*.*")))
        if filename is None:
            return

        json = jsonserializer.read_json_file(filename)
        calculator = CalculatorDeserializer().deserialize(json)

        self.calculator.px.set(calculator.px.get())
        self.calculator.h.set(calculator.h.get())
        self.calculator.coord.set(calculator.coord.get())

    def save_conf_file(self):
        filename=filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if filename is None:
            return
        json = jsonserializer.serialize_data(self.calculator)
        jsonserializer.save_json_file(json, filename.name)

    def h_updated(self, matrix):
        self.view.set_homography_matrix(matrix)

    def coord_updated(self, coords):
        self.view.set_coord_entries(coords)

    def calculate_homography(self):
        coords = np.zeros((4,2), dtype=np.float32)
        iterables = [range(0, coords.shape[0]), range(0, coords.shape[1])]
        for n, (i, j) in enumerate(itertools.product(*iterables)):
            coords[i][j]=self.view.entries_coord[n].get()
        self.calculator.coord.set(coords, callbacks=False)
        self.calculator.calculate_h()

    def change_mousse_loc(self, event):
        x, y = event.x/self.view.img.size[0], event.y/self.view.img.size[1]
        point = self.calculator.get_real_mousse_loc((x,y))
        self.view.set_mousse_loc(point)

    def update_point_loc(self, event):
        x, y = event.x / self.view.img.size[0], event.y / self.view.img.size[1]
        self.calculator.update_point_loc((x,y), self.view.point_selected)

    def change_image_diag(self):
        filename = filedialog.askopenfile(initialdir = "'/home/jisern/repositories/homography-calibrator/src/", title = "Select file",
                                          filetypes = (("jpeg files","*.jpg"),
                                                       ("png files","*.png"),
                                                       ("all files","*.*")))
        if filename is None:
            return
        self.change_image(filename.name)

    def change_image(self, filename):
        img = Image.open(filename)
        self.calculator.change_image(filename, img)

    def image_changed(self, image):
        self.view.set_image(image.filename, image.img)

    def point_updated(self, points):
        self.view.set_point_loc(points)