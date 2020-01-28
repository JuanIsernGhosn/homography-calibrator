from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image
import os

MAP_TYPES = ['roadmap', 'terrain', 'satellite', 'hybrid']
POINT_ICONS = ['../../media/squared_cursor_red.png', '../../media/squared_cursor_blue.png',
               '../../media/squared_cursor_green.png', '../../media/squared_cursor_magent.png']

class MapViewer(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.set_GUI()

    def set_GUI(self):
        vcmd = (self.register(validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        map_info_form = Frame(self, borderwidth=1, relief="raised")

        label_lat = ttk.Label(map_info_form, text="Latitude:", padding=(5, 5))
        label_lon = ttk.Label(map_info_form, text="Longitude:", padding=(5, 5))
        self.entry_lat = Entry(map_info_form, width=11, validate='key', validatecommand=vcmd,
                               textvariable=StringVar().set(0))
        self.entry_lon = Entry(map_info_form, width=11, validate='key', validatecommand=vcmd,
                               textvariable=StringVar().set(0))
        self.search_button = Button(map_info_form, text="Search")
        self.set_coordinates(0.0, 0.0)

        self.zoom_slidder = Scale(map_info_form, from_=0, to=22, orient=HORIZONTAL)
        label_lat.pack(side=LEFT)
        self.entry_lat.pack(side=LEFT)
        label_lon.pack(side=LEFT)
        self.entry_lon.pack(side=LEFT)
        self.search_button.pack(side=LEFT, padx=5)
        self.zoom_slidder.pack(side=LEFT, padx=32)
        map_info_form.pack(fill=BOTH)
        self.panel_bird_view_image = tk.Canvas(self, width=640, height=640, bd=0, highlightthickness=0,
                                               relief='ridge')

        map_type_section = Frame(self)
        self.map_type_rbs = []
        self.map_type_var = StringVar()

        for i, map_type in enumerate(MAP_TYPES):
            rb = Radiobutton(map_type_section, text=map_type, value=map_type, var=self.map_type_var)
            rb.grid(column=i, row=0)
            self.map_type_rbs.append(rb)

        self.panel_bird_view_image.pack(anchor=N)
        map_type_section.pack()

    def set_image(self, img):
        photo = ImageTk.PhotoImage(img)
        self.panel_bird_view_image.create_image(0, 0, anchor=NW, image=photo)
        self.panel_bird_view_image.image = photo

    def set_zoom_slidder(self, value):
        self.zoom_slidder.set(value)

    def set_map_type_rb(self, value):
        self.map_type_var.set(value)

    def set_coordinates(self, lat, lon):
        insert_entry_without_validation(self.entry_lat, lat)
        insert_entry_without_validation(self.entry_lon, lon)

    def update_coord_marks(self, points):
        self.panel_bird_view_image.icons = []
        for i, (img_point_loc, icon) in enumerate(zip(points, POINT_ICONS)):
            script_dir = os.path.dirname(__file__)
            icon_path = os.path.join(script_dir, icon)
            photo = ImageTk.PhotoImage(Image.open(icon_path))
            icon_center = (photo.width() / 2, photo.height() / 2)
            self.panel_bird_view_image.icons.append(photo)
            self.panel_bird_view_image.create_image(
                (int(img_point_loc[0] - icon_center[0]), int(img_point_loc[1] - icon_center[1])),
                image=self.panel_bird_view_image.icons[i], anchor='nw')

    def update_per_marks(self, perimeters):
        self.panel_bird_view_image.create_image(0, 0, anchor=NW, image=self.panel_bird_view_image.image)
        for perimeter in perimeters:
            perimeter = list(sum(perimeter, ()))
            if not perimeter: continue
            self.panel_bird_view_image.create_polygon(perimeter, outline='#f11', fill='#1f1', width=1)


def insert_entry_without_validation(entry, value):
    entry.config(validate="none")
    entry.delete(0, END)
    entry.insert(0, value)
    entry.configure(validate="key")


def validate(action, index, value_if_allowed,
             prior_value, text, validation_type, trigger_type, widget_name):
    if value_if_allowed:
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            return False
    else:
        return False
