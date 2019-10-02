from src.Model.homographycalculator import HomographyCalculator
import numpy as np

class CalculatorDeserializer:
    def deserialize(self, json):
        calculator = HomographyCalculator()
        calculator.px.set(np.array(json['px'], dtype=np.float32))
        calculator.h.set(np.array(json['h_matrix'], dtype=np.float32))
        calculator.coord.set(np.array(json['coord'], dtype=np.float32))

        return calculator




