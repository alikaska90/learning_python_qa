from src.Figure import Figure
from math import pi


class Circle(Figure):
    def __init__(self, radius):
        super().__init__([radius])
        self.name = f'Circle with radius {radius}'
        self.radius = radius

    @property
    def area(self):
        return pi * self.radius ** 2

    @property
    def perimeter(self):
        return 2 * pi * self.radius
