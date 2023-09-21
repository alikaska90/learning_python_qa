import pytest

from src.Triangle import Triangle


@pytest.mark.parametrize(("side_a", "side_b", "side_c", "area", "perimeter"),
                         [(5, 5, 8, 12, 18),
                          (5, 5, 5, 10.83, 15),
                          (4, 9, 6, 9.56, 19),
                          (5.98, 6.5, 4.1, 11.98, 16.58)],
                         ids=["isosceles triangle",
                              "equilateral triangle",
                              "scalene triangle",
                              "float sides"])
def test_triangle_positive(side_a, side_b, side_c, area, perimeter):

    """Test for methods of Triangle class with correct input data"""

    triangle = Triangle(side_a, side_b, side_c)
    assert triangle.name == f"Triangle with sides {side_a}, {side_b} and {side_c}"
    assert round(triangle.area, 2) == area
    assert triangle.perimeter == perimeter


@pytest.mark.parametrize(("side_a", "side_b", "side_c"),
                         [(10, 3, 4),
                          (3.5, 8.25, 4.02),
                          (6, 6, 15),
                          (3, 2, 1)],
                         ids=["side a more then sum of sides b and c",
                              "side b more then sum of sides a and c",
                              "side c more then sum of sides a and b",
                              "side a equal sum of sides b and c"])
def test_is_not_triangle(side_a, side_b, side_c):

    """Check that Triangle can't be created with incorrect values of sides"""

    with pytest.raises(ValueError) as excinfo:
        triangle = Triangle(side_a, side_b, side_c)

    assert "There is no triangle with declared sides" in str(excinfo.value)


@pytest.mark.parametrize(("side_a", "side_b", "side_c"),
                         [(-4, 9, 6),
                          (4, 0, 6),
                          (4, 9, "1")],
                         ids=["negative value in side a",
                              "0 in side b",
                              "string in side c"])
def test_triangle_negative(side_a, side_b, side_c):

    """Check ValueError raise
    if Triangle is created with incorrect values of sides"""

    with pytest.raises(ValueError) as excinfo:
        triangle = Triangle(side_a, side_b, side_c)

    assert "Figure sides or circle radius must be positive numbers" in str(excinfo.value)
