from src.controller import Controller
from tkinter import Tk

def main():
    root = Tk()
    app = Controller(root)
    app.change_image('/home/jisern/repositories/homography-calibrator/src/title_image.jpg')
    app.view.root.mainloop()
    return 0

if __name__ == '__main__':
    main()
