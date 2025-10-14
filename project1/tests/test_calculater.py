import math
import pytest

from project1.calculater import (
    add,
    divide,
    factorial,
    evaluate_expression,
)


def test_add():
    assert add(2, 3) == 5.0


def test_divide():
    assert divide(10, 2) == 5.0
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


def test_factorial():
    assert factorial(5) == math.factorial(5)
    with pytest.raises(ValueError):
        factorial(3.5)


def test_evaluate_expression_basic():
    assert evaluate_expression("5 * 4 + 2 + 3 / 4 + 5 - 7") == pytest.approx(
        5 * 4 + 2 + 3 / 4 + 5 - 7
    )


def test_evaluate_expression_math_functions():
    assert evaluate_expression("sin(30) + log10(100) - sqrt(16)") == pytest.approx(
        math.sin(math.radians(30)) + math.log10(100) - math.sqrt(16)
    )


def test_evaluate_with_memory():
    m = evaluate_expression("2 + 2")
    assert evaluate_expression("M * 3", memory=m) == 12
