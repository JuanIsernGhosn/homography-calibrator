from src.Controller.controller import Controller
from tkinter import Tk

def main():
    root = Tk()
    app = Controller(root)
    app.change_camera_image('/home/jisern/repositories/homography-calibrator/media/title_image.jpg')
    app.change_bird_view_image(lat=41.85, lon=-87.65, zoom=14, maptype="satellite")
    app.view.root.mainloop()
    return 0

if __name__ == '__main__':
    main()
