import pytest

from src.Circle import Circle


@pytest.mark.parametrize(("radius", "area", "perimeter"),
                         [(8, 201.062, 50.265),
                          (6.3, 124.690, 39.584)],
                         ids=["integer radius",
                              "float radius"])
def test_circle_positive(radius, area, perimeter):

    """Test for methods of Circle class with correct input data"""

    circle = Circle(radius)
    assert circle.name == f"Circle with radius {radius}"
    assert round(circle.area, 3) == area
    assert round(circle.perimeter, 3) == perimeter


@pytest.mark.parametrize("radius",
                         [-15, 0, False, "9"],
                         ids=["radius is negative value",
                              "radius equal 0",
                              "radius is bool value",
                              "radius is string"])
def test_circle_negative(radius):

    """Check ValueError raise
    if Circle is created with incorrect radius value"""

    with pytest.raises(ValueError) as excinfo:
        circle = Circle(radius)

    assert "Figure sides or circle radius must be positive numbers" in str(excinfo.value)
