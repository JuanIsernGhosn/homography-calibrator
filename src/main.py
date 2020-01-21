from Controller.controller import Controller
from tkinter import Tk

def main():
    root = Tk()
    app = Controller(root)
    app.change_camera_image('../media/title_image.jpg')
    app.change_bird_view_image(lat=37.200176, lon=-3.604003, zoom=20, maptype="satellite")
    app.view.root.mainloop()
    return 0

if __name__ == '__main__':
    main()
