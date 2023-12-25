from enum import Enum
from argparse import ArgumentParser

from config import config, MyEnum


def readable_types(type_name: str) -> str:
    """
    Заменяет входящие типы на строки, указанные в словаре, если такой нет - возвращает исходный тип
    :param type_name: Строка с названием типа
    :return: Читабельное представление типа
    """
    readable = {'bool': 'Логическое значение (True/False)',
                'str': 'Строковое значение',
                'int': 'Целочисленное значение',
                'float': 'Число с плавающей точкой (1.345))'}
    readable_name = readable.get(type_name)
    return readable_name if readable_name else type_name


def readable_rule(rule: str) -> str:
    """
    Заменяет текст во входящих правилах
    :param rule: Правило
    :return: Измененное правило
    """
    readable = {'InRange': 'Диапазон числа',
                'Min': 'Минимальное значение',
                'Max': 'Максимальное значение',
                'Match': 'Регулярное выражение'}
    for key, value in readable.items():
        rule = rule.replace(key, value)
    return rule


def formatter(data: dict, show_hint: bool, show_rules: bool, show_secret: bool, is_primitive=False, depth=0) -> str:
    """
    Преобразует входящее поле в поле вида:
        Name: retention_days
        Label: Срок хранения .log файлов
        Type: int
        Rule: Min(1)
        Default: 7
    для примитивного поля и в поле вида:
        Name: profile
        Label: Настройки профиля
        Type: class(profile)
        Default: None
    для поля, не являющегося примитивным
    :param show_secret:
    :param data: входные данные
    :param show_hint: отображать описание полей
    :param show_rules: отображать правила полей (работает только с примитивными полями)
    :param depth: коэффициент отступа (4 пробела * depth)
    :param is_primitive: является ли поле примитивным
    :return:
    """
    indentation = "    " * depth
    result = f"{indentation}Название поля: {data.get('name')}\n"
    if data.get('label'):
        result += f"{indentation}Описание поля: {data.get('label')}\n"
    if show_hint and data.get('hint'):
        result += f"{indentation}Подсказка: {data.get('hint')}\n"
    if show_secret and data.get('secret'):
        result += f"{indentation}Секретное поле\n"
    if is_primitive:
        if data.get('is_iterable'):
            result += f"{indentation}Тип поля: Список({readable_types(data.get('type'))})\n"
        else:
            result += f"{indentation}Тип поля: {readable_types(data.get('type'))}\n"
        if show_rules and data.get('rule'):
            result += f"{indentation}Правила: {readable_rule(data.get('rule'))}\n"
    else:
        result += f"{indentation}Тип поля: класс({data.get('name')})\n"
    if data.get('default'):
        if isinstance(data.get('default'), Enum):
            data['default'] = data.get('default').value
        result += f"{indentation}Значение по умолчанию: {data.get('default')}\n"
    return result


def parse(data: dict, show_hint: bool, show_secret: bool, show_rules: bool, show_primitive_only: bool, depth=0) -> str:
    """
    Разбирает метадату конфигураций, путем рекурсивного путешествия вглубь структуры,
    по ходу выполнения формирует строку вида:
        Name: log
        Label: Параметры логирования
        Type: class(log)
        Default: None

                Name: retention_days
                Label: Срок хранения .log файлов
                Type: int
                Rule: Min(1)
                Default: 7

                Name: level
                Label: Уровень логирования
                Type: int
                Rule: InRange((0, 10))
                Default: 3
    :param data: Входные данные (dict)
    :param show_hint: Отображение описания полей
    :param show_secret: Отображение секретных полей
    :param show_rules: Отображение правил
    :param show_primitive_only: Отображение только примитивных полей
    :param depth: коэффициент отступа (4 пробела * depth)
    :return: Распаршенные данные, в виде описания конфигурации
    """
    result = ''
    if data.get('is_primitive') is None:
        while data:
            _name, value = data.popitem()
            is_primitive = value.get('is_primitive')
            if not value.get('secret') or show_secret:
                if not show_primitive_only or (show_primitive_only and is_primitive):
                    result += formatter(data=value,
                                        show_hint=show_hint,
                                        show_rules=show_rules,
                                        show_secret=show_secret,
                                        is_primitive=is_primitive,
                                        depth=depth * (not show_primitive_only)) + "\n"
                if not is_primitive:
                    result += parse(data=value.get('type'),
                                    show_hint=show_hint,
                                    show_secret=show_secret,
                                    show_rules=show_rules,
                                    show_primitive_only=show_primitive_only,
                                    depth=depth + 1)
    return result


if __name__ == "__main__":
    arg_parser = ArgumentParser(prog='MetaData Parser')
    arg_parser.add_argument('-sh', '--show-hint', default=False, required=False,
                            action='store_true', help='отображать подсказки полей')
    arg_parser.add_argument('-ss', '--show-secret', default=False, required=False,
                            action='store_true', help='отображать скрытые поля')
    arg_parser.add_argument('-sr', '--show-rules', default=False, required=False,
                            action='store_true', help='отображать правила')
    arg_parser.add_argument('-p', '--primitive', default=False, required=False,
                            action='store_true', help='отображать только примитивные поля')
    arg_parser.add_argument('-o', '--out', type=str, required=False, help='название файла для записи')
    args = arg_parser.parse_args()
    parsed_data = parse(data=config.__metadata__(),
                        show_hint=args.show_hint,
                        show_secret=args.show_secret,
                        show_rules=args.show_rules,
                        show_primitive_only=args.primitive)
    print(parsed_data)
    if args.out:
        open(args.out, 'w', encoding='utf-8').write(parsed_data)
