from src.View.appgui import ApplicationGUI
from src.Model.homographycalculator import HomographyCalculator
from src.Model.perimetermanager import PerimeterManager
from Model.birdcalculator import BirdCalculator
from src.Model.JSON.modeldeserializer import HomographyDeserializer, PerimetersDeserializer
from tkinter import filedialog
from PIL import Image
from src.Model.JSON import jsonserializer
import itertools
import webbrowser
import numpy as np

REPO_URL = "https://github.com/JuanIsernGhosn/homography-calibrator/blob/master/README.md"

class Controller:
    def __init__(self, root):
        self.view = ApplicationGUI(root)
        self.view.menu1.entryconfigure('Open image', command=self.change_image_diag)
        self.view.menu1.entryconfigure('Load camera config.', command=self.load_conf_file)
        self.view.menu1.entryconfigure('Save camera config.', command=self.save_conf_file)
        self.view.menu1.entryconfigure('Load perimeter config.', command=self.load_per_file)
        self.view.menu1.entryconfigure('Save perimeter config.', command=self.save_per_file)
        self.view.menu2.entryconfigure('Documentation', command=go_to_documentation_action)
        self.view.button_homography.configure(command=self.calculate_homography)

        self.homo_calculator = HomographyCalculator()
        self.homo_calculator.image.addCallback(self.camera_image_changed)
        self.homo_calculator.px.addCallback(self.point_updated)
        self.homo_calculator.h.addCallback(self.h_updated)
        self.homo_calculator.px_bird.addCallback(self.coord_point_updated)
        self.homo_calculator.coord.addCallback(self.coord_updated)

        self.per_manager = PerimeterManager()
        self.per_manager.perimeters_px.addCallback(self.per_updated)

        self.homo_bird_viewer = BirdCalculator()
        self.homo_bird_viewer.map.addCallback(self.homo_bird_view_image_changed)
        self.view.homo_viewer.zoom_slidder.configure(command=self.change_homo_zoom)
        for rb in self.view.homo_viewer.map_type_rbs:
            rb.configure(command=self.change_homo_map_type)
        self.view.homo_viewer.search_button.configure(command=self.change_homo_coords)

        self.per_bird_viewer = BirdCalculator()
        self.per_bird_viewer.map.addCallback(self.peri_bird_view_image_changed)
        self.view.per_viewer.zoom_slidder.configure(command=self.change_per_zoom)
        for rb in self.view.per_viewer.map_type_rbs:
            rb.configure(command=self.change_per_map_type)
        self.view.per_viewer.search_button.configure(command=self.change_per_coords)

        self.view.per_add_bt.configure(command=self.add_per)
        self.view.per_rm_bt.configure(command=self.rm_per)

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
        homo_calculator, bird_calculator = HomographyDeserializer().deserialize(json)

        self.homo_calculator.px.set(homo_calculator.px.get())
        self.homo_calculator.h.set(homo_calculator.h.get())
        self.homo_calculator.coord.set(homo_calculator.coord.get())
        self.homo_calculator.px_bird.set(homo_calculator.px_bird.get())

        self.homo_bird_viewer.map.set(bird_calculator.map.get())

    def save_conf_file(self):
        filename=filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if filename is None:
            return
        json = jsonserializer.serialize_homo_data(self.homo_calculator, self.homo_bird_viewer)
        jsonserializer.save_json_file(json, filename.name)

    def load_per_file(self):
        filename = filedialog.askopenfilename(initialdir=".",
                                              title="Open perimeters file",
                                              filetypes= (("txt files","*.txt"),
                                                           ("all files","*.*")))
        if filename is None:
            return

        json = jsonserializer.read_json_file(filename)
        per_manager, bird_calculator = PerimetersDeserializer().deserialize(json)

        self.per_manager.perimeters.set(per_manager.perimeters.get())
        self.per_manager.perimeters_px.set(per_manager.perimeters_px.get())

        self.per_bird_viewer.map.set(bird_calculator.map.get())

    def save_per_file(self):
        filename=filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if filename is None:
            return
        json = jsonserializer.serialize_per_data(self.per_manager, self.per_bird_viewer)
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
        self.homo_calculator.coord.set(coords, callbacks=False)
        self.homo_calculator.calculate_h()

    def change_mousse_loc(self, event):
        x, y = event.x / self.view.cam_img.size[0], event.y / self.view.cam_img.size[1]
        point = self.homo_calculator.get_real_mousse_loc((x, y))
        self.view.set_mousse_loc(point)

    def update_point_loc(self, event):
        x, y = event.x / self.view.cam_img.size[0], event.y / self.view.cam_img.size[1]
        self.homo_calculator.update_point_loc((x, y), self.view.point_selected)

    def update_point_coords(self, event):
        (lat, lon) = self.homo_bird_viewer.get_coord_from_px((event.x, event.y))
        self.homo_calculator.update_coords((lat, lon), self.view.point_selected)
        self.homo_calculator.update_point_coords((event.x, event.y), self.view.point_selected)

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
        self.homo_calculator.change_image(filename, self.img)

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

        self.view.homo_viewer.update_coord_marks(self.homo_calculator.px_bird.get())

    def peri_bird_view_image_changed(self, map):
        self.view.per_viewer.set_image(map.img)
        self.view.per_viewer.set_zoom_slidder(map.zoom)
        self.view.per_viewer.set_map_type_rb(map.map_type)
        self.view.per_viewer.set_coordinates(map.lat, map.lon)

        self.view.per_viewer.update_per_marks(self.per_manager.perimeters_px.get())

    def point_updated(self, points):
        self.view.set_point_loc(points)
        self.view.update_point_marks(points, (self.homo_calculator.image.get().height, self.homo_calculator.image.get().width))

    def change_homo_zoom(self, event):
        self.homo_bird_viewer.change_zoom(int(event))
        self.homo_calculator.reset_coords()
        self.homo_calculator.reset_px_bird()

    def change_per_zoom(self, event):
        self.per_bird_viewer.change_zoom(int(event))
        self.per_manager.reset_per()

    def add_per(self):
        self.per_manager.add_perimeter()

    def rm_per(self):
        selection =  self.view.per_list.curselection()
        if selection:
            self.per_manager.remove_perimeters(selection)

    def change_homo_map_type(self):
        map_type = self.view.homo_viewer.map_type_var.get()
        self.homo_bird_viewer.change_map_type(map_type)

    def change_per_map_type(self):
        map_type = self.view.per_viewer.map_type_var.get()
        self.per_bird_viewer.change_map_type(map_type)

    def change_homo_coords(self):
        latitude = self.view.homo_viewer.entry_lat.get()
        longitude = self.view.homo_viewer.entry_lon.get()
        self.homo_bird_viewer.change_map_coords(latitude, longitude)

        self.homo_calculator.reset_coords()
        self.homo_calculator.reset_px_bird()

    def change_per_coords(self):
        latitude = self.view.per_viewer.entry_lat.get()
        longitude = self.view.per_viewer.entry_lon.get()
        self.per_bird_viewer.change_map_coords(latitude, longitude)

    def update_perimeters(self, event):
        coord = self.per_bird_viewer.get_coord_from_px((event.x, event.y))
        self.per_manager.add_point(coord, (event.x, event.y), self.view.per_list.curselection())

    def per_updated(self, perimeters_px):
        perimeters = self.per_manager.perimeters.get()
        self.view.per_updated(perimeters_px, perimeters)


def go_to_documentation_action():
    webbrowser.open(REPO_URL)
