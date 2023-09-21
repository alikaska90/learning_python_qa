from src.Rectangle import Rectangle


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)
        self.name = f'Square with side {side}'
