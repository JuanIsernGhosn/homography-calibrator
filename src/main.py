#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk, font
import getpass


# Gestor de geometría (grid). Ventana dimensionable

class Aplication():
    def __init__(self):

        # Basic options
        self.root = Tk()
        self.root.title("Homography calibrator")
        self.root.option_add("*Font", "Helvetica 12")  # Fuente predeterminada
        self.root.option_add('*tearOff', False)  # Deshabilita submenús flotantes
        #self.root.attributes('-fullscreen', True)  # Maximiza ventana completa
        self.root.minsize(400, 300)  # Establece tamaño minimo ventana

        # Menu bar
        menubar = Menu(self.root)
        self.root['menu'] = menubar
        menu1 = Menu(menubar)
        menu2 = Menu(menubar)
        menubar.add_cascade(menu=menu1, label='File')
        menubar.add_cascade(menu=menu2, label='Help')
        menu1.add_command(label='Open image',underline=0, accelerator="Ctrl+o",compound=LEFT)
        menu1.add_separator()
        menu1.add_command(label='Load config. file',underline=0,accelerator="Ctrl+f",compound=LEFT)
        menu1.add_command(label='Save config. file', underline=0,compound=LEFT)

        # Tab manager
        tab_parent = ttk.Notebook(self.root)
        tab_homography=ttk.Frame(tab_parent)
        tab_perimeters=ttk.Frame(tab_parent)
        tab_parent.add(tab_homography, text='Homography')
        tab_parent.add(tab_perimeters, text='Perimeters')

        # Homography tab
        label_file = Label(tab_homography, text='File:')
        image_name_variable_text = StringVar()
        label_image_name = Label(tab_homography, textvariable=image_name_variable_text)

        self.marco = ttk.Frame(self.raiz, borderwidth=2,
                               relief="raised", padding=(10, 10))

        # Define el resto de widgets pero en este caso el primer
        # paràmetro indica que se situarán en el widget del
        # marco anterior 'self.marco'.

        self.etiq1 = ttk.Label(self.marco, text="Usuario:",
                               font=fuente, padding=(5, 5))
        self.etiq2 = ttk.Label(self.marco, text="Contraseña:",
                               font=fuente, padding=(5, 5))


        label_file.place(x=10, y=10)
        label_image_name.place(x=50, y=10)

        tab_parent.pack(expand=1, fill='both')

        self.root.mainloop()

def main():
    mi_app = Aplication()
    return 0

if __name__ == '__main__':
    main()
