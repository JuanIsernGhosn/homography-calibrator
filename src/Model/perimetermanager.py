from Model.observable import Observable


class PerimeterManager:

    def __init__(self):
        self.perimeters = Observable([])
        self.perimeters_px = Observable([])

    def add_perimeter(self):
        perimeters = self.perimeters.get()
        perimeters.append([])
        self.perimeters.set(perimeters)

        perimeters_px = self.perimeters_px.get()
        perimeters_px.append([])
        self.perimeters_px.set(perimeters_px)

    def add_point(self, coord, point, indexes):
        perimeters = self.perimeters.get()
        perimeters_px = self.perimeters_px.get()
        indexes = list(indexes)

        if not perimeters:
            return

        for index in indexes:
            perimeters[index].append(coord)
            perimeters_px[index].append(point)
            self.perimeters.set(perimeters)
            self.perimeters_px.set(perimeters_px)

    def remove_perimeters(self, indexes):
        for index in indexes:
            self.remove_perimeter(index)

    def remove_perimeter(self, index):
        perimeters = self.perimeters.get()
        perimeters_px = self.perimeters_px.get()
        del perimeters[index]
        del perimeters_px[index]
        self.perimeters.set(perimeters)
        self.perimeters_px.set(perimeters_px)

    def reset_per(self):
        self.perimeters.set([])
        self.perimeters_px.set([])
