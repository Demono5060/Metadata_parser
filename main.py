from config import config


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
    result += f"{indentation}Описание поля: {data.get('label')}\n"
    if show_hint:
        result += f"{indentation}Подсказка: {data.get('hint')}\n"
    if show_secret:
        result += f"{indentation}Секретное поле\n"
    if is_primitive:
        result += f"{indentation}Тип поля: {data.get('type')}\n"
        if show_rules:
            result += f"{indentation}Правила: {data.get('rule')}\n"
    else:
        result += f"{indentation}Тип поля: класс({data.get('name')})\n"
    result += f"{indentation}Значение по стандарту: {data.get('default')}\n"
    return result


def parse(data: dict, show_hint: bool, show_secret: bool, show_rules: bool, depth=0) -> str:
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
    :param depth: коэффициент отступа (4 пробела * depth)
    :return: Распаршенные данные, в виде описания конфигурации
    """
    result = ''
    if data.get('is_primitive') is None:
        while data:
            name, value = data.popitem()
            is_primitive = value.get('is_primitive')
            if is_primitive and (not value.get('is_secret') or show_secret):
                result += formatter(data=value,
                                    show_hint=show_hint,
                                    show_rules=show_rules,
                                    show_secret=show_secret,
                                    is_primitive=is_primitive,
                                    depth=depth + 1) + "\n"
            else:
                result += formatter(data=value,
                                    show_hint=show_hint,
                                    show_rules=show_rules,
                                    show_secret=show_secret,
                                    is_primitive=is_primitive,
                                    depth=depth)
                result += '\n'
                result += parse(data=value.get('type'),
                                show_hint=show_hint,
                                show_secret=show_secret,
                                show_rules=show_rules,
                                depth=depth + 1)
    return result


if __name__ == "__main__":
    show_hint = True
    show_secret = True
    show_rules = True
    parsed_data = parse(data=config.__metadata__(),
                        show_hint=show_hint,
                        show_secret=show_secret,
                        show_rules=show_rules)

    parsed_data = parsed_data.replace(' None\n', ' Пусто\n')
    parsed_data = parsed_data.replace(' int\n', " Целое чисто\n")
    parsed_data = parsed_data.replace(' bool\n', " Логическое значение (True/False)\n")
    parsed_data = parsed_data.replace(' str\n', " Строка\n")
    parsed_data = parsed_data.replace('InRange', "Диапазон числа ")
    parsed_data = parsed_data.replace('Min', "Минимальное значение")
    parsed_data = parsed_data.replace('Max', "Максимальное значение")
    parsed_data = parsed_data.replace('Match', "Регулярное выражение")

    print(parsed_data)
    open("out.txt", 'w').write(parsed_data)
