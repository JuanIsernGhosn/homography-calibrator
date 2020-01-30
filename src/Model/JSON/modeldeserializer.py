from src.Model.homographycalculator import HomographyCalculator
from src.Model.perimetermanager import PerimeterManager
from src.Model.birdcalculator import BirdCalculator
import numpy as np
import ast


class HomographyDeserializer:

    def deserialize(self, json):
        homo_calculator = HomographyCalculator()
        homo_calculator.px.set(np.array(json['camera_marks_px'], dtype=np.float32))
        homo_calculator.h.set(np.array(json['h_matrix'], dtype=np.float32))
        homo_calculator.coord.set(np.array(json['coord'], dtype=np.float32))
        homo_calculator.px_bird.set(np.array(json['map_marks_px'], dtype=np.float32))

        bird_calculator = BirdCalculator()
        (lat, lon) = json['map_coord']
        zoom = json['map_zoom']
        bird_calculator.change_map(lat, lon, zoom)

        return homo_calculator, bird_calculator


class PerimetersDeserializer:

    def deserialize(self, json):
        per_manager = PerimeterManager()
        perimeters_px = ast.literal_eval(json['perimeters_px'])
        perimeters = ast.literal_eval(json['perimeters'])
        per_manager.perimeters.set(perimeters)
        per_manager.perimeters_px.set(perimeters_px)

        bird_calculator = BirdCalculator()
        (lat, lon) = json['map_coord']
        zoom = json['map_zoom']
        bird_calculator.change_map(lat, lon, zoom)

        return per_manager, bird_calculator
