# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk, filedialog
import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
import itertools
import os
from View.scrollableframe import ScrollableFrame
from View.mapviewer import MapViewer

POINT_ICONS = ['../../media/squared_cursor_red.png', '../../media/squared_cursor_blue.png',
               '../../media/squared_cursor_green.png', '../../media/squared_cursor_magent.png']

class ApplicationGUI():

    def __init__(self, root):
        self.root = root
        self.set_basic_options()
        self.set_GUI()
        self.set_commands()
        h = np.zeros((3,3))
        self.set_homography_matrix(h)

    def set_basic_options(self):
        self.root.title("Homography calibrator")
        self.root.option_add("*Font", "Helvetica 12")  # Fuente predeterminada
        self.root.option_add('*tearOff', False)  # Deshabilita submenús flotantes
        self.root.minsize(1200, 800)  # Establece tamaño minimo ventana
        self.root.attributes('-fullscreen', True)
        self.point_selected = 0

    def set_commands(self):
        pass
        #self.panel_image.bind('<Motion>', self.motion)

    def set_GUI(self):

        vcmd = (self.root.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        menubar = Menu(self.root)
        self.root['menu'] = menubar
        self.menu1 = Menu(menubar)
        self.menu2 = Menu(menubar)
        menubar.add_cascade(menu=self.menu1, label='File')
        menubar.add_cascade(menu=self.menu2, label='Help')
        self.menu1.add_command(label='Open image', underline=0, compound=LEFT)
        self.menu1.add_separator()
        self.menu1.add_command(label='Load config. file', underline=0, compound=LEFT)
        self.menu1.add_command(label='Save config. file', underline=0, compound=LEFT)

        # Tab manager
        tab_parent = ttk.Notebook(self.root)
        tab_homography = Frame(tab_parent)
        tab_perimeters = Frame(tab_parent)
        tab_parent.add(tab_homography, text='Homography')
        tab_parent.add(tab_perimeters, text='Perimeters')
        homography_content = ScrollableFrame(tab_homography)

        frame_img_info = ttk.Frame(homography_content.scrollable_frame, borderwidth=2, relief="raised")
        label_filename = ttk.Label(frame_img_info, text="File:", padding=(5, 5))
        self.label_filename_var = ttk.Label(frame_img_info, text="filename", padding=(5, 5))
        label_pixel_loc = ttk.Label(frame_img_info, text="(X, Y):", padding=(5, 5))
        self.label_pixel_loc_var = ttk.Label(frame_img_info, text="(0, 0)", padding=(5, 5))
        label_filename.pack(side=LEFT)
        self.label_filename_var.pack(side=LEFT)
        self.label_pixel_loc_var.pack(side=RIGHT)
        label_pixel_loc.pack(side=RIGHT)
        frame_img_info.pack(fill=X, anchor=N)

        # Views section
        view_section = Frame(homography_content.scrollable_frame, borderwidth=1, relief="raised")
        view_group_section = Frame(view_section)

        # Camera view section
        camera_view = Frame(view_group_section)

        # Bird view section
        self.homo_viewer = MapViewer(view_group_section)

        self.panel_camera_canvas = tk.Canvas(camera_view, width=800, height=600, bd=0, highlightthickness=0, relief='ridge')

        view_group_section.pack(anchor=N)
        view_section.pack(fill='both', anchor=N)
        camera_view.pack(side=LEFT, padx=5)
        self.homo_viewer.pack(anchor=NE, padx=5)

        self.panel_camera_canvas.pack(anchor=N)


        ## Homography information
        homog_section = Frame(homography_content.scrollable_frame, borderwidth=1, relief="raised")
        info_group_section = Frame(homog_section)

        # Homography points (Radio buttons)
        grid_points = Frame(info_group_section, borderwidth=1, relief="raised")

        Label(grid_points, text='Image location').grid(row=0, column=1, pady=2, rowspan=2)

        MODES = [("Point 1", 0),("Point 2", 1),("Point 3", 2),("Point 4", 3)]
        v = StringVar()
        v.set(0)

        def select_point():
            self.point_selected=v.get()

        for i, (text, mode) in enumerate(MODES):
            b = Radiobutton(grid_points, text=text, variable=v, value=mode, indicatoron=0, command=select_point)
            b.grid(row=i+2, column=0, sticky=W, pady=2)

        # Homography points (Labels for location)
        self.labels_points = []
        for i in range(0,4):
            label_point = Label(grid_points, text='(0, 0)')
            label_point.grid(row=i+2, column=1, pady=2)
            self.labels_points.append(label_point)

        # Homography points (Coordinate entries)
        Label(grid_points, text='Coordinates').grid(row=0, column=2, pady=2, columnspan=2)
        Label(grid_points, text='Lat.').grid(row=1, column=2, pady=2)
        Label(grid_points, text='Lon.').grid(row=1, column=3, pady=2)

        iterables = [range(0, 4), range(0, 2)]
        self.entries_coord = []
        for n, (i, j) in enumerate(itertools.product(*iterables)):
            self.entries_coord.append(Entry(grid_points, width=11, validate='key', validatecommand=vcmd, textvariable=StringVar().set(0)))
            self.entries_coord[n].insert(0, '0.0')
            self.entries_coord[n].grid(row=i+2, column=j+2, pady=2)

        # Calculate homography button
        self.button_homography=Button(grid_points, text ="Calculate Homography")
        self.button_homography.grid(row=len(MODES)+2, columnspan=4)
        grid_points.pack(side=LEFT, padx=5, pady=30)

        ## Homography matrix preview
        grid_matrix = Frame(info_group_section, borderwidth=1, relief="raised")
        iterables = [range(0, 3), range(0, 3)]
        Label(grid_matrix,text='Homography Matrix').grid(row=0, column=0, columnspan=3, pady=15)
        self.labels_h = []
        for (i, j) in itertools.product(*iterables):
            lab = Label(grid_matrix, text='0.0')
            lab.grid(row=1+i, column=j, pady=10)
            self.labels_h.append(lab)
        grid_matrix.pack(anchor=NE, padx=5, pady=30)

        info_group_section.pack(anchor=N)
        homog_section.pack(fill='both', anchor=N)

        homography_content.pack(fill='both', expand=True)

        self.per_viewer = MapViewer(tab_perimeters)
        self.per_viewer.pack(anchor=NE, padx=5)


        tab_parent.pack(expand=1, fill='both')

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    def set_coord_entries(self, coords):
        iterables = [range(0, coords.shape[0]), range(0, coords.shape[1])]
        for n, (i, j) in enumerate(itertools.product(*iterables)):
            self.entries_coord[n].config(validate="none")
            self.entries_coord[n].delete(0, END)
            self.entries_coord[n].insert(0,str(coords[i][j]))
            self.entries_coord[n].config(validate="key")

    def set_homography_matrix(self, matrix):
        iterables = [range(0, 3), range(0, 3)]
        for n, (i, j) in enumerate(itertools.product(*iterables)):
            self.labels_h[n].configure(text=str('%.10f'%(matrix[i][j])))

    def set_camera_image(self, filename, img):
        self.cam_img=img
        self.filename=filename

        mywidth=800
        wpercent = (mywidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))

        self.cam_img = img.resize((mywidth, hsize), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(self.cam_img)

        self.panel_camera_canvas.config(width=mywidth, height=hsize)

        self.panel_camera_canvas.create_image(0, 0, anchor=NW, image=photo)
        self.panel_camera_canvas.image = photo

        self.label_filename_var.configure(text=filename)

    def set_mousse_loc(self, point):
        self.label_pixel_loc_var.configure(text='('+str(round(point[0]))+', '+str(round(point[1]))+')')

    def set_point_loc(self, points):
        for n in range(0, 4):
            self.labels_points[n].configure(text='(' + str(int(round(points[n][0])))+', '+str(int(round(points[n][1]))) + ')')

    def update_point_marks(self, points, img_size):

        self.panel_camera_canvas.icons = []

        for i, (img_point_loc, icon) in enumerate(zip(self.get_img_point_loc(points, img_size), POINT_ICONS)):
            script_dir = os.path.dirname(__file__)
            icon_path = os.path.join(script_dir, icon)
            photo = ImageTk.PhotoImage(Image.open(icon_path))
            icon_center = (photo.width()/2, photo.height()/2)
            self.panel_camera_canvas.icons.append(photo)
            self.panel_camera_canvas.create_image((int(img_point_loc[0]-icon_center[0]), int(img_point_loc[1]-icon_center[1])),
                                                  image=self.panel_camera_canvas.icons[i], anchor='nw')

    def update_coord_marks(self, points):
        self.homo_viewer.update_coord_marks(points)

    def get_img_point_loc(self, points, img_size):
        puntos = points.copy()
        puntos[:, 0] = puntos[:, 0] / img_size[1] * self.panel_camera_canvas.winfo_width()
        puntos[:, 1] = puntos[:, 1] / img_size[0] * self.panel_camera_canvas.winfo_height()
        return puntos

    def draw_point_marks(self, points):
        img = PhotoImage(file='media/squared_cursor.png')
        self.create_image(250, 250, image=img)

    def set_coordinates(self, lat, lon):
        self.homo_viewer.set_coordinates(lat, lon)


def insert_entry_without_validation(entry, value):
    entry.config(validate="none")
    entry.delete(0, END)
    entry.insert(0, value)
    entry.configure(validate="key")
