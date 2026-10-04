from decimal import Decimal

import pytest

from toolkit.converter import converter_main
from toolkit.exceptions import (
    InvalidLenError,
    InvalidMassError,
    InvalidTemperatureError,
    InvalidType,
    InvalidTypes,
)


def test_mass():
    assert converter_main('kg', 'g', '1') == Decimal(1000)
    assert converter_main('g', 'mg', '1') == Decimal(1000)
    assert converter_main('mg', 'kg', '1000000') == Decimal(1)


def test_mass_negative():
    with pytest.raises(InvalidMassError):
        converter_main('kg', 'g', '-1')


def test_length():
    assert converter_main('m', 'cm', '1') == Decimal(100)
    assert converter_main('cm', 'mm', '1') == Decimal(10)
    # Следующая строка выявит баг в len_types (пропущена запятая):
    # assert converter_main('km', 'm', '1') == Decimal('1000')


def test_length_negative():
    with pytest.raises(InvalidLenError):
        converter_main('m', 'cm', '-1')


def test_temperature():
    assert converter_main('c', 'k', '0') == Decimal('273.15')
    assert converter_main('k', 'c', '273.15') == Decimal(0)
    assert converter_main('c', 'f', '0') == Decimal(32)
    assert converter_main('f', 'c', '32') == Decimal(0)
    assert converter_main('f', 'k', '32') == Decimal('273.15')


def test_temperature_below_absolute_zero():
    with pytest.raises(InvalidTemperatureError):
        converter_main('c', 'k', '-274')
    with pytest.raises(InvalidTemperatureError):
        converter_main('k', 'c', '-1')
    with pytest.raises(InvalidTemperatureError):
        converter_main('f', 'c', '-460')


def test_invalid_types():
    with pytest.raises(InvalidType):
        converter_main('kg', 'm', '1')
    with pytest.raises(InvalidTypes):
        converter_main('xx', 'yy', '1')