# ТЗ: calc "exp"        convert val --from unit --to unit       --help

import argparse
from sys import exit

from .calculating import calculator_main
from .converter import converter_main


def main():
    parser = argparse.ArgumentParser(description='Калькулятор и конвертер величин. Конвертер поддерживает следующие приставки из СИ:'
                                                 'k (кило-), g (гекто-), da (дека-), d (деци-), c (санти-), m (милли-')

    parser.add_argument('mode',type=str, help="Режим работы программы. convert - для конвертера. calc - для калькулятора" )
    parser.add_argument("--from", type=str, dest='from_unit', help="Из какой величины конвертировать (для mode=convert)")
    parser.add_argument("--to", type=str, dest='to_unit', help="В какую величину конвертировать (для mode=convert)")
    parser.add_argument('expression', type=str,
                        help='Выражение (для mode=calc это выражение, для mode=converter - значение)')

    args = parser.parse_args()
    if args.mode == 'calc':
        try:
            print(calculator_main(args.expression))
            exit(0)
        except Exception as e:
            print(e)
            exit(2)
    elif args.mode == 'convert':
        try:
            print(converter_main(args.from_unit, args.to_unit, args.expression))
            exit(0)
        except Exception as e:
            print(e)
            exit(2)
    else:
        print("Неизвестный режим")
        exit(2)


if '__main__' == __name__:
    main()
