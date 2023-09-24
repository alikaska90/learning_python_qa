from src.Figure import Figure


class Rectangle(Figure):

    def __init__(self, side_a, side_b):
        super().__init__([side_a, side_b])
        self.name = f'Rectangle with sides {side_a} and {side_b}'
        self.side_a = side_a
        self.side_b = side_b

    @property
    def area(self):
        return self.side_a * self.side_b

    @property
    def perimeter(self):
        return 2 * (self.side_a + self.side_b)
