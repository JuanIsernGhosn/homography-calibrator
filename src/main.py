# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
from src.homographycalculator import HomographyCalculator
import getpass

class Application():

    def __init__(self, root):
        self.root = root
        self.set_basic_options()
        self.set_GUI()
        self.set_commands()

        filename = 'VIRAT_S_0503.jpg'
        img = Image.open(filename)
        self.set_image(filename, img)

    def set_basic_options(self):
        self.root.title("Homography calibrator")
        self.root.option_add("*Font", "Helvetica 12")  # Fuente predeterminada
        self.root.option_add('*tearOff', False)  # Deshabilita submenús flotantes
        self.root.minsize(1200, 800)  # Establece tamaño minimo ventana
        self.point_selected = 0

    def set_commands(self):
        pass
        #self.panel_image.bind('<Motion>', self.motion)

    def set_GUI(self):
        menubar = Menu(self.root)
        self.root['menu'] = menubar
        self.menu1 = Menu(menubar)
        self.menu2 = Menu(menubar)
        menubar.add_cascade(menu=self.menu1, label='File')
        menubar.add_cascade(menu=self.menu2, label='Help')
        self.menu1.add_command(label='Open image',underline=0, accelerator="Ctrl+o",compound=LEFT)
        self.menu1.add_separator()
        self.menu1.add_command(label='Load config. file',underline=0,accelerator="Ctrl+f",compound=LEFT)
        self.menu1.add_command(label='Save config. file', underline=0,compound=LEFT)

        # Tab manager
        tab_parent = ttk.Notebook(self.root)
        tab_homography = Frame(tab_parent)
        tab_perimeters = Frame(tab_parent)
        tab_parent.add(tab_homography, text='Homography')
        tab_parent.add(tab_perimeters, text='Perimeters')

        # Image info frame
        frame_img_info = ttk.Frame(tab_homography, borderwidth=2, relief="raised")
        label_filename = ttk.Label(frame_img_info, text="File:", padding=(5, 5))
        self.label_filename_var = ttk.Label(frame_img_info, text="filename", padding=(5, 5))
        label_pixel_loc = ttk.Label(frame_img_info, text="(X, Y):", padding=(5, 5))
        self.label_pixel_loc_var = ttk.Label(frame_img_info, text="(0, 0)", padding=(5, 5))
        label_filename.pack(side=LEFT)
        self.label_filename_var.pack(side=LEFT)
        self.label_pixel_loc_var.pack(side=RIGHT)
        label_pixel_loc.pack(side=RIGHT)
        frame_img_info.pack(fill=X, anchor=N)

        # Image view
        frame_img = Frame(tab_homography, borderwidth=1, relief="raised")
        self.panel_image = Label(frame_img, borderwidth=0)
        frame_img.pack(fill=X, anchor=N)
        self.panel_image.pack(anchor=N)

        # Homography points
        frame_points = Frame(tab_homography, borderwidth=1, relief="raised")
        grid_points = Frame(frame_points, borderwidth=1, relief="raised")

        MODES = [("Point 1", 0),("Point 2", 1),("Point 3", 2),("Point 4", 3)]

        v = StringVar()
        v.set(0)

        def select_point():
            self.point_selected=v.get()

        for i, (text, mode) in enumerate(MODES):
            b = Radiobutton(grid_points, text=text, variable=v, value=mode, indicatoron=0, command=select_point)
            b.grid(row=i+1, column=0, sticky=W, pady=2)

        b = Label(grid_points, text='Image location')
        b.grid(row=0, column=1, pady=2)

        for i in range(0,len(MODES)):
            b = Label(grid_points, text='(0, 0)')
            b.grid(row=i+1, column=1, pady=2)

        b = Label(grid_points, text='Coordinates (X, Y, Z=0)')
        b.grid(row=0, column=2, pady=2)

        for i in range(0,len(MODES)):
            b = Entry(grid_points)
            b.insert(0, '0.0, 0.0')
            b.grid(row=i+1, column=2, pady=2)

        b=Button(grid_points, text ="Calculate Homography")
        b.grid(row=len(MODES)+1, columnspan=3)

        grid_points.pack(padx=50, pady=30)
        frame_points.pack(fill=X, anchor=N)

        tab_parent.pack(expand=1, fill='both')

    def set_image(self, filename, img):
        self.img=img
        self.filename=filename
        mywidth=800
        wpercent = (mywidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        self.img = img.resize((mywidth, hsize), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(self.img)
        self.panel_image.configure(image=photo)
        self.panel_image.image=photo
        self.label_filename_var.configure(text=filename)

    def set_mousse_loc(self, point):
        self.label_pixel_loc_var.configure(text='('+str(point[0])+', '+str(point[1])+')')

    def set_point_loc(self, point):
        print('('+str(point[0])+', '+str(point[1])+')')

class Controller:
    def __init__(self, root):
        self.view = Application(root)

        self.view.menu1.entryconfigure('Open image', command=self.change_image)
        self.calculator = HomographyCalculator(self.view.filename, self.view.img)

        self.calculator.image.addCallback(self.image_changed)
        self.view.panel_image.bind('<Motion>', self.change_mousse_loc)
        self.view.panel_image.bind('<Button-1>', self.change_point_loc)

    def change_mousse_loc(self, event):
        x, y = event.x/self.view.img.size[0], event.y/self.view.img.size[1]
        point = self.calculator.get_real_mousse_loc((x,y))
        self.view.set_mousse_loc(point)

    def update_point_loc(self, event):
        x, y = event.x / self.view.img.size[0], event.y / self.view.img.size[1]
        self.calculator.update_point_loc((x,y))
        self.view.set_point_loc(point)

    def change_image(self):
        filename = filedialog.askopenfilename(initialdir = "'/home/jisern/repositories/homography-calibrator/src/", title = "Select file",
                                              filetypes = (("jpeg files","*.jpg"),
                                                           ("png files","*.png"),
                                                           ("all files","*.*")))
        img = Image.open(filename)
        self.calculator.change_image(filename, img)

    def image_changed(self, image):
        self.view.set_image(image.filename, image.img)







def main():
    root = Tk()
    #root.withdraw()
    app = Controller(root)
    app.view.root.mainloop()
    return 0

if __name__ == '__main__':
    main()
