import pytest

from src.Rectangle import Rectangle


@pytest.mark.parametrize(("side_a", "side_b", "area", "perimeter"),
                         [(5, 8, 40, 26),
                          (10.5, 3.87, 40.635, 28.74)],
                         ids=["integer sides",
                              "float sides"])
def test_rectangle_positive(side_a, side_b, area, perimeter):

    """Test for methods of Rectangle class with correct input data"""

    rectangle = Rectangle(side_a, side_b)
    assert rectangle.name == f"Rectangle with sides {side_a} and {side_b}"
    assert rectangle.area == pytest.approx(area)
    assert rectangle.perimeter == pytest.approx(perimeter)


@pytest.mark.parametrize(("side_a", "side_b"),
                         [(-15, 5),
                          (8, 0),
                          (True, 10.99),
                          (7.1, "11")],
                         ids=["negative value in side a",
                              "0 in side b",
                              "bool value in side a",
                              "string in side b"])
def test_rectangle_negative(side_a, side_b):

    """Check ValueError raise
    if Rectangle is created with incorrect values of sides"""

    with pytest.raises(ValueError) as excinfo:
        rectangle = Rectangle(side_a, side_b)

    assert "Figure sides or circle radius must be positive numbers" in str(excinfo.value)
