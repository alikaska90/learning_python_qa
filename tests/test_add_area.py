import pytest

from src.Circle import Circle
from src.Rectangle import Rectangle
from src.Square import Square
from src.Triangle import Triangle


@pytest.mark.parametrize(("figure_1", "figure_2", "expected"),
                         [(Circle(5), Rectangle(3, 10), 108.54),
                          (Rectangle(7.5, 3.22), Square(4), 40.15),
                          (Square(8.3), Triangle(3, 4, 5), 74.89),
                          (Triangle(5, 5, 8), Circle(3.3), 46.212)],
                         ids=["add area for circle and rectangle",
                              "add area for rectangle and square",
                              "add area for square and triangle",
                              "add area for triangle and circle"])
def test_add_area_positive(figure_1, figure_2, expected):

    """Test for add_area method with correct input data.
    Check the following combinations of figures:
    1. Circle and Rectangle;
    2. Rectangle and Square;
    3. Square and Triangle;
    4. Triangle and Circle."""

    assert round(figure_1.add_area(figure_2), 3) == expected


@pytest.mark.parametrize(("figure", "value"),
                         [(Circle(5), 123),
                          (Rectangle(3, 7), "123"),
                          (Triangle(5, 5, 8), True),
                          (Square(6), [1, 2])],
                         ids=["add area with integer argument",
                              "add area with string argument",
                              "add area with bool argument",
                              "add area with list argument"])
def test_add_area_negative(figure, value):

    """Test for add_area method with incorrect input data.
    Check integer, string, bool, list arguments of add_area method."""

    with pytest.raises(ValueError) as excinfo:
        figure.add_area(value)

    assert "This object is not figure" in str(excinfo.value)
