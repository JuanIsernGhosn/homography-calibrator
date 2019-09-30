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

    def set_basic_options(self):
        self.root.title("Homography calibrator")
        self.root.option_add("*Font", "Helvetica 12")  # Fuente predeterminada
        self.root.option_add('*tearOff', False)  # Deshabilita submenús flotantes
        self.root.minsize(800, 800)  # Establece tamaño minimo ventana

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
        label_filename_var = ttk.Label(frame_img_info, text="filename", padding=(5, 5))
        label_pixel_loc = ttk.Label(frame_img_info, text="X,Y:", padding=(5, 5))
        label_pixel_loc_var = ttk.Label(frame_img_info, text="(0,0)", padding=(5, 5))
        label_filename.pack(side=LEFT)
        label_filename_var.pack(side=LEFT)
        label_pixel_loc_var.pack(side=RIGHT)
        label_pixel_loc.pack(side=RIGHT)
        frame_img_info.pack(fill=X, anchor=N)

        
        # Image view
        frame_img = ttk.Frame(tab_homography, borderwidth=1, relief="raised")
        img = Image.open('VIRAT_S_0503.jpg')
        photo = ImageTk.PhotoImage(img)
        panel_image = Label(frame_img, image=photo, width=600, height=400)
        frame_img.pack(fill=X, anchor=N)
        panel_image.pack(anchor=N)

        tab_parent.pack(expand=1, fill='both')
        #self.root.mainloop()


class Controller:
    def __init__(self, root):
        self.calculator = HomographyCalculator()
        self.view = Application(root)
        self.view.menu1.entryconfigure('Open image', command=self.change_image)

    def change_image(self):
        filename = filedialog.askopenfilename(initialdir = "/", title = "Select file",
                                              filetypes = (("jpeg files","*.jpg"),
                                                           ("png files","*.png"),
                                                           ("all files","*.*")))
        self.calculator.set







def main():
    root = Tk()
    #root.withdraw()
    app = Controller(root)
    root.mainloop()
    return 0

if __name__ == '__main__':
    main()
