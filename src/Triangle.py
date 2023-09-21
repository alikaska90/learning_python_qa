from src.Figure import Figure


class Triangle(Figure):
    def __init__(self, side_a, side_b, side_c):
        super().__init__([side_a, side_b, side_c])
        self.name = f'Triangle with sides {side_a}, {side_b} and {side_c}'
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c
        if not self.is_triangle:
            raise ValueError("There is no triangle with declared sides")

    @property
    def area(self):
        p = self.perimeter / 2
        return (p * (p - self.side_a) * (p - self.side_b) * (p - self.side_c)) ** 0.5

    @property
    def perimeter(self):
        return self.side_a + self.side_b + self.side_c

    @property
    def is_triangle(self):
        if self.side_a >= (self.side_b + self.side_c) or \
                self.side_b >= (self.side_a + self.side_c) or \
                self.side_c >= (self.side_a + self.side_b):
            return False

        return True
