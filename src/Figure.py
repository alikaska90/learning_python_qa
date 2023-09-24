from abc import ABC, abstractmethod


class Figure(ABC):
    def __init__(self, values):
        self.values = values
        self.check_values()

    @abstractmethod
    def area(self):
        pass

    def add_area(self, other_figure):
        if not isinstance(other_figure, Figure):
            raise ValueError("This object is not figure")
        return self.area + other_figure.area

    def check_values(self):
        for value in self.values:
            if not isinstance(value, (int, float)) or \
                    isinstance(value, bool) or \
                    value <= 0:
                raise ValueError("Figure sides or circle radius must be positive numbers")
