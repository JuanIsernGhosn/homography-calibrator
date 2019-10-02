class Image:
    def __init__(self, filename, img):
        self.filename = filename
        self.img = img
        self.width = None if img is None else img.size[0]
        self.height = None if img is None else img.size[1]