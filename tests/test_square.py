import pytest

from src.Square import Square


@pytest.mark.parametrize(("side", "area", "perimeter"),
                         [(8, 64, 32),
                          (3.5, 12.25, 14)],
                         ids=["integer side",
                              "float side"])
def test_square_positive(side, area, perimeter):

    """Test for methods of Square class with correct input data"""

    square = Square(side)
    assert square.name == f"Square with side {side}"
    assert square.area == area
    assert square.perimeter == perimeter


@pytest.mark.parametrize("side",
                         [-3, 0, False, "3.15"],
                         ids=["side is negative value",
                              "side equal 0",
                              "side is bool value",
                              "side is string"])
def test_square_negative(side):

    """Check ValueError raise
    if Square is created with incorrect side value"""

    with pytest.raises(ValueError) as excinfo:
        square = Square(side)

    assert "Figure sides or circle radius must be positive numbers" in str(excinfo.value)
