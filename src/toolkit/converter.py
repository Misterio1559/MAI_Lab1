from decimal import ROUND_HALF_UP, Decimal, getcontext

from .exceptions import (
    InvalidLenError,
    InvalidMassError,
    InvalidTemperatureError,
    InvalidType,
    InvalidTypes,
)

mass_types = ['mg', 'cg', 'dg', 'g', 'dag', 'gg', 'kg']
len_types = ['mm', 'cm', 'dm', 'm', 'dam', 'gm', 'km']
temperature_types = ['c', 'k', 'f']
getcontext().prec = 10
getcontext().rounding = ROUND_HALF_UP


def converter_main(type1: str, type2: str, value: str) -> Decimal:
    value = Decimal(value)

    curr_type = check_types(type1, type2)   # Общий для двух единиц измерения тип

    if curr_type == 'mass':
        return  mass_converter(type1, type2, value)
    elif curr_type == 'len':
        return  len_converter(type1, type2, value)
    else:       # curr_type == 'temp':
        return  temperature_converter(type1, type2, value)

def get_type(type1: str):
    if type1 in mass_types:
        return 'mass'
    elif type1 in len_types:
        return 'len'
    elif type1 in temperature_types:
        return 'temp'
    return 'invalid'

# Вспомогательный инструмент для получения строки по типу для конструирования текста ошибки
def invalid_type_constructor(checked: str) -> str:
    if checked == 'invalid':
        return 'неизвестную величину'
    elif checked == 'mass':
        return  'массу'
    elif checked == 'len':
        return  'длинну'
    else:       # checked == 'temp':
        return  'температуру'

def check_types(type1: str, type2: str) -> str:
    checked_type1 = get_type(type1)     # checked_ - тип единицы измерения
    checked_type2 = get_type(type2)
    if checked_type1 == 'invalid' and checked_type2 == 'invalid':
        raise InvalidTypes('Неизвестные единицы измерения "' + type1 + '" и "' + type2 + '"!')
    if checked_type1 == checked_type2:
        return checked_type1

    raise InvalidType('Введённая вами первая единица измерения обозначает ' + invalid_type_constructor(checked_type1) \
             + ', в то время как вторая единица измерения обозначает' + invalid_type_constructor(checked_type2) + '!')


def mass_converter(type1: str, type2: str, value1: Decimal) -> Decimal:
    if value1 < 0:
        raise InvalidMassError("Введена отрицательная масса!")

    if type1 in mass_types and type2 in mass_types:
        ind1 = mass_types.index(type1)
        ind2 = mass_types.index(type2)
        return value1 * Decimal(10) ** (ind1 - ind2)

    raise InvalidType("Неизвестная единица измерения массы: " + type1 if type1 not in mass_types else type2)


def len_converter(type1: str, type2: str, value1: Decimal) -> Decimal:
    if value1 < 0:
        raise InvalidLenError("Введена отрицательная длинна!")

    ind1 = len_types.index(type1)
    ind2 = len_types.index(type2)
    return value1 * Decimal(10) ** (ind1 - ind2)


def temperature_converter(type1: str, type2: str, value1: Decimal) -> Decimal:
    if type1 == 'c' and value1 < -273.15 or type1 == 'k' and value1 < 0 or type1 == 'f' and value1 < -459.67:
        raise InvalidTemperatureError("Введена температура ниже абсолютного нуля!")

    if type1 == type2:
        return value1
    if type1 == 'c' and type2 == 'k':
        return value1 + Decimal('273.15')
    elif type1 == 'k' and type2 == 'c':
        return value1 - Decimal('273.15')
    elif type1 == 'c' and type2 == 'f':
        return value1 * Decimal('1.8') + Decimal(32)
    elif type1 == 'k' and type2 == 'f':
        return value1 * 1.8 - Decimal('459.67')        # (value1 - 273.15) * 1.8 + 32 = value1 * 1.8 - 273.15 * 1.8 + 32
    elif type1 == 'f' and type2 == 'c':
        return Decimal(5) / Decimal(9) * (value1 - 32)
    else:       # type1 == 'f' and type2 == 'k'
        return Decimal(5) / Decimal(9) * Decimal(value1 - 32) + Decimal('273.15')