from decimal import Decimal

import pytest

from toolkit.calculating import calculator_main
from toolkit.exceptions import CalculationError, OrderError, SymbolError


def test_plus():
    assert calculator_main("1+2") == Decimal(3)


def test_plus_multiplication():
    assert calculator_main("2+3*4") == Decimal(14)
    assert calculator_main("2*3+4") == Decimal(10)


def test_division():
    assert calculator_main("10/2") == Decimal(5)


def test_unary():
    assert calculator_main("-5+3") == Decimal(-2)
    assert calculator_main("2*-3") == Decimal(-6)
    assert calculator_main("1--2") == Decimal(3)
    assert calculator_main("1+-2") == Decimal(-1)


def test_order_errors():
    with pytest.raises(OrderError):
        calculator_main("+")
    with pytest.raises(OrderError):
        calculator_main("1+")
    with pytest.raises(OrderError):
        calculator_main("1+++2")
    with pytest.raises(OrderError):
        calculator_main("1 2")

def test_percent():
    assert calculator_main("5+10%3") == Decimal("6")
    assert calculator_main("10%3*2") == Decimal("2")
    assert calculator_main("2*10%3") == Decimal("2")

def test_division2():
    assert calculator_main("5//2") == Decimal("2")
    assert calculator_main("111//1") == Decimal("111")
    assert calculator_main("23//12") == Decimal("1")

def test_symbol_error():
    with pytest.raises(SymbolError):
        calculator_main("1+a")

def test_calculation_error():
    with pytest.raises(CalculationError):
        calculator_main("1/0")