from decimal import ROUND_HALF_UP, Decimal, InvalidOperation, getcontext

from .exceptions import CalculationError, OrderError, SymbolError

operations = list('+-*/|%')
getcontext().prec = 10
getcontext().rounding = ROUND_HALF_UP

def calculator_main(data: str) -> Decimal:
    data = tokenezation(data)
    data = unary_validation(data)
    checker(data)
    data = calculate_converter(data)
    return calculation(data)

def tokenezation(data: str) -> list[str]:
    data = data.replace('-', ' - ')
    data = data.replace('+', ' + ')
    data = data.replace('*', ' * ')
    data = data.replace('//', ' | ') # | - значок для деления нацело
    data = data.replace('/', ' / ')
    data = data.replace('%', ' % ')
    data = data.split()
    return data

def unary_validation(data: list[str]) -> list[str]:
    res = []
    i = 1
    if len(data) <= 1:
        raise OrderError("Подано слишком короткое выражение")
    if data[0] == '-' and data[1] not in operations:
        res.append('-' + data[1])
        i += 1
    elif data[0] == '+' and data[1] not in operations:
        res.append(data[1])
        i += 1
    else:
        res.append(data[0])
    while i < len(data) - 1:
        if data[i] == '-' and data[i - 1] in operations and data[i + 1] not in operations:
            res.append('-' + data[i + 1])
            i += 1
        elif data[i] == '+' and data[i - 1] in operations and data[i + 1] not in operations:
            res.append(data[i + 1])
            i += 1
        else:
            res.append(data[i])
        i += 1
    if i != len(data):
        res.append(data[-1])
    return res

def calculate_converter(data: list[str]) -> list[str|Decimal]:
    res = []
    for i in data:
        if i in operations:
            res.append(i)
        else:
            res.append(Decimal(i))
    return res

def checker(data: list[str]):
    flag = True

    if data[0] in operations:
        raise OrderError("Первый элемент является символом оператора. Вычисление значения невозможно")

    if data[-1] in operations:
        raise OrderError("Последний элемент является символом оператора. Вычисление значения невозможно")

    for i in range(len(data)):
        if data[i] in operations:
            if flag:
                raise OrderError(f"Было подано подряд два символа операторов в положении {i}:{i + 1}. Вычисление значения невозможно")
            flag = True
        else:
            try:
                Decimal(data[i])
            except InvalidOperation as _:
                raise SymbolError(f"{i + 1} элемент не является ни числом, ни оператором, допустимым к использованию")
            if not flag:
                raise OrderError(f"Было подано подряд два числа в положении {i}:{i + 1}. Вычисление значения невозможно")
            flag = False


def calculation(mass: list[str|Decimal]) -> Decimal:
    i = 1
    try:
        while i < len(mass) - 1:
            if mass[i] == '*':
                mass[i] = mass[i - 1] * mass[i + 1]
                del mass[i + 1]
                del mass[i - 1]
                i -= 1
                continue
            elif mass[i] == '/':
                mass[i] = mass[i - 1] / mass[i + 1]
                del mass[i + 1]
                del mass[i - 1]
                i -= 1
                continue
            elif mass[i] == '|':
                mass[i] = mass[i - 1] // mass[i + 1]
                del mass[i + 1]
                del mass[i - 1]
                i -= 1
                continue
            elif mass[i] == '%':
                mass[i] = mass[i - 1] % mass[i + 1]
                del mass[i + 1]
                del mass[i - 1]
                i -= 1
                continue
            i += 1
        i = 1
        while i < len(mass) - 1:
            if mass[i] == '+':
                mass[i] = mass[i - 1] + mass[i + 1]
                del mass[i + 1]
                del mass[i - 1]
                i -= 1
                continue
            elif mass[i] == '-':
                mass[i] = mass[i - 1] - mass[i + 1]
                del mass[i + 1]
                del mass[i - 1]
                i -= 1
                continue
            i += 1
    except Exception:
        raise CalculationError("При вычислении значения выражения произошла ошибка")
    if len(mass) > 1:
        raise CalculationError("Была подана некорректная строка!")
    return mass[0]
