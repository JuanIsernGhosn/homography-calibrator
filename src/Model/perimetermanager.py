from Model.observable import Observable


class PerimeterManager:

    def __init__(self):
        self.perimeters = Observable([])
        self.index = 0

    def add_perimeter(self, first_point):
        new_per = [first_point]
        perimeters = self.perimeters.get()
        perimeters.append(new_per)
        self.perimeters.set(perimeters)

    def add_point(self, point):
        perimeters = self.perimeters.get()
        if not perimeters:
            self.add_perimeter(point)
        else:
            perimeters = self.perimeters.get()
            perimeters[self.index].append(point)
            self.perimeters.set(perimeters)

    def remove_perimeter(self, index):
        self.perimeters.set(self.perimeters.get().remove(index))
        self.index -= 1

    def close_perimeter(self):
        self.index += 1