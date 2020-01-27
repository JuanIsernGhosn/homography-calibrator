from src.View.appgui import ApplicationGUI
from src.Model.homographycalculator import HomographyCalculator
from src.Model.perimetermanager import PerimeterManager
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
        self.calculator.px_bird.addCallback(self.coord_point_updated)
        self.calculator.coord.addCallback(self.coord_updated)

        self.per_manager = PerimeterManager()
        self.per_manager.perimeters.addCallback(self.per_updated)

        self.homo_bird_viewer = BirdViewer()
        self.homo_bird_viewer.map.addCallback(self.homo_bird_view_image_changed)
        self.view.homo_viewer.zoom_slidder.configure(command=self.change_homo_zoom)
        for rb in self.view.homo_viewer.map_type_rbs:
            rb.configure(command=self.change_map_type)
        self.view.homo_viewer.search_button.configure(command=self.change_homo_coords)

        self.per_bird_viewer = BirdViewer()
        self.per_bird_viewer.map.addCallback(self.peri_bird_view_image_changed)
        self.view.per_viewer.zoom_slidder.configure(command=self.change_per_zoom)
        for rb in self.view.per_viewer.map_type_rbs:
            rb.configure(command=self.change_map_type)
        self.view.per_viewer.search_button.configure(command=self.change_per_coords)

        self.view.panel_camera_canvas.bind('<Motion>', self.change_mousse_loc)
        self.view.panel_camera_canvas.bind('<Button-1>', self.update_point_loc)
        self.view.homo_viewer.panel_bird_view_image.bind('<Button-1>', self.update_point_coords)
        self.view.per_viewer.panel_bird_view_image.bind('<Button-1>', self.update_perimeters)

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

    def coord_point_updated(self, points):
        self.view.update_coord_marks(points)

    def coords_to_px(self, coords):
        for coord in coords:
            print(self.homo_bird_viewer.get_px_from_coord(coord))

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
        (lat, lon) = self.homo_bird_viewer.get_coord_from_px((event.x, event.y))
        self.calculator.update_coords((lat, lon), self.view.point_selected)
        self.calculator.update_point_coords((event.x, event.y), self.view.point_selected)

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

    def change_homo_bird_view_image(self, lat, lon, zoom, maptype):
        self.homo_bird_viewer.change_map(lat, lon, zoom, maptype)

    def change_peri_bird_view_image(self, lat, lon, zoom, maptype):
        self.per_bird_viewer.change_map(lat, lon, zoom, maptype)

    def homo_bird_view_image_changed(self, map):
        self.view.homo_viewer.set_image(map.img)
        self.view.homo_viewer.set_zoom_slidder(map.zoom)
        self.view.homo_viewer.set_map_type_rb(map.map_type)
        self.view.homo_viewer.set_coordinates(map.lat, map.lon)

        self.view.homo_viewer.update_coord_marks(self.calculator.px_bird.get())

    def peri_bird_view_image_changed(self, map):
        self.view.per_viewer.set_image(map.img)
        self.view.per_viewer.set_zoom_slidder(map.zoom)
        self.view.per_viewer.set_map_type_rb(map.map_type)
        self.view.per_viewer.set_coordinates(map.lat, map.lon)

        self.view.per_viewer.update_coord_marks(self.calculator.px_bird.get())

    def point_updated(self, points):
        self.view.set_point_loc(points)
        self.view.update_point_marks(points, (self.calculator.image.get().height, self.calculator.image.get().width))

    def change_homo_zoom(self, event):
        self.homo_bird_viewer.change_zoom(int(event))
        self.calculator.reset_coords()
        self.calculator.reset_px_bird()

    def change_per_zoom(self, event):
        self.per_bird_viewer.change_zoom(int(event))


    def change_map_type(self):
        map_type = self.view.homo_viewer.map_type_var.get()
        self.homo_bird_viewer.change_map_type(map_type)

    def change_homo_coords(self):
        latitude = self.view.homo_viewer.entry_lat.get()
        longitude = self.view.homo_viewer.entry_lon.get()
        self.homo_bird_viewer.change_map_coords(latitude, longitude)

        self.calculator.reset_coords()
        self.calculator.reset_px_bird()

    def change_per_coords(self):
        latitude = self.view.per_viewer.entry_lat.get()
        longitude = self.view.per_viewer.entry_lon.get()
        self.per_bird_viewer.change_map_coords(latitude, longitude)

    def update_perimeters(self, event):
        self.per_manager.add_point((event.x, event.y))

    def per_updated(self, perimeters):
        self.view.per_viewer.per_updated(perimeters)
