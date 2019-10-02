from src.controller import Controller
from tkinter import Tk

def main():
    root = Tk()
    app = Controller(root)
    app.change_image('VIRAT_S_0503.jpg')
    app.view.root.mainloop()
    return 0

if __name__ == '__main__':
    main()
