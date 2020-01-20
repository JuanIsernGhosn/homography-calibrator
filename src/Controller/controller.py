from src.View.appgui import ApplicationGUI
from src.Model.homographycalculator import HomographyCalculator
from Model.birdviewer import BirdViewer
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
        self.calculator.image.addCallback(self.camera_image_changed)
        self.calculator.px.addCallback(self.point_updated)
        self.calculator.h.addCallback(self.h_updated)
        self.calculator.coord.addCallback(self.coord_updated)

        self.bird_viewer = BirdViewer()
        self.bird_viewer.map.addCallback(self.bird_view_image_changed)
        self.view.zoom_slidder.configure(command=self.change_zoom)
        for rb in self.view.map_type_rbs:
            rb.configure(command=self.change_map_type)
        self.view.search_button.configure(command=self.change_coords)

        self.view.panel_camera_canvas.bind('<Motion>', self.change_mousse_loc)
        self.view.panel_camera_canvas.bind('<Button-1>', self.update_point_loc)
        self.view.panel_bird_view_image.bind('<Button-1>', self.update_point_coords)

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
        px_coords = self.coords_to_px(coords)
        self.view.update_coord_marks(px_coords)

    def coords_to_px(self, coords):
        for coord in coords:
            print(self.bird_viewer.get_px_from_coord(coord))


    def calculate_homography(self):
        coords = np.zeros((4,2), dtype=np.float32)
        iterables = [range(0, coords.shape[0]), range(0, coords.shape[1])]
        for n, (i, j) in enumerate(itertools.product(*iterables)):
            coords[i][j]=self.view.entries_coord[n].get()
        self.calculator.coord.set(coords, callbacks=False)
        self.calculator.calculate_h()

    def change_mousse_loc(self, event):
        x, y = event.x / self.view.cam_img.size[0], event.y / self.view.cam_img.size[1]
        point = self.calculator.get_real_mousse_loc((x,y))
        self.view.set_mousse_loc(point)

    def update_point_loc(self, event):
        x, y = event.x / self.view.cam_img.size[0], event.y / self.view.cam_img.size[1]
        self.calculator.update_point_loc((x,y), self.view.point_selected)

    def update_point_coords(self, event):
        (lat, lon) = self.bird_viewer.get_coord_from_px((event.x, event.y))
        self.calculator.update_point_coords((lat,lon), self.view.point_selected)

    def change_image_diag(self):
        filename = filedialog.askopenfile(initialdir = "'/home/jisern/repositories/homography-calibrator/src/", title = "Select file",
                                          filetypes = (("jpeg files","*.jpg"),
                                                       ("png files","*.png"),
                                                       ("all files","*.*")))
        if filename is None:
            return
        self.change_camera_image(filename.name)

    def change_camera_image(self, filename):
        self.img = Image.open(filename)
        self.calculator.change_image(filename, self.img)

    def camera_image_changed(self, image):
        self.view.set_camera_image(image.filename, image.img)

    def change_bird_view_image(self, lat, lon, zoom, maptype):
        self.bird_viewer.change_map(lat, lon, zoom, maptype)

    def bird_view_image_changed(self, map):
        self.view.set_bird_view_image(map.img)
        self.view.set_zoom_slidder(map.zoom)
        self.view.set_map_type_rb(map.map_type)
        self.view.set_coordinates(map.lat, map.lon)

    def point_updated(self, points):
        self.view.set_point_loc(points)
        self.view.update_point_marks(points, (self.calculator.image.get().height, self.calculator.image.get().width))

    def change_zoom(self, event):
        self.bird_viewer.change_zoom(int(event))

    def change_map_type(self):
        map_type = self.view.map_type_var.get()
        self.bird_viewer.change_map_type(map_type)

    def change_coords(self):
        latitude = self.view.entry_lat.get()
        longitude = self.view.entry_lon.get()
        self.bird_viewer.change_map_coords(latitude, longitude)

