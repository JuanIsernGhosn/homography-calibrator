from Controller.controller import Controller
from tkinter import Tk

def main():
    root = Tk()
    app = Controller(root)
    app.change_camera_image('../media/title_image.jpg')
    app.change_homo_bird_view_image(lat=0, lon=0, zoom=1, maptype="satellite")
    app.change_peri_bird_view_image(lat=0, lon=0, zoom=1, maptype="satellite")
    app.view.root.mainloop()
    return 0

if __name__ == '__main__':
    main()
