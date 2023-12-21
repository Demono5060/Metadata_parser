from config import config


def formatter(data: dict, show_label: bool, show_rules: bool, depth=0, is_primitive=False) -> str:
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
    :param data: входные данные
    :param show_label: отображать описание полей
    :param show_rules: отображать правила полей (работает только с примитивными полями)
    :param depth: коэффициент отступа (4 пробела * depth)
    :param is_primitive: является ли поле примитивным
    :return:
    """
    indentation = "    " * depth
    result = f"{indentation}Нвазвание поля: {data.get('name')}\n"
    if show_label:
        result += f"{indentation}Описание поля: {data.get('label')}\n"
    if is_primitive:
        result += f"{indentation}Тип поля: {data.get('type')}\n"
        if show_rules:
            result += f"{indentation}Правила: {data.get('rule')}\n"
    else:
        result += f"{indentation}Тип поля: класс({data.get('name')})\n"
    result += f"{indentation}Значение по стандарту: {data.get('default')}\n"
    return result


def parse(data: dict, show_label: bool, show_secret: bool, show_rules: bool, depth=0) -> str:
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
    :param show_label: Отображение описания полей
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
                                    show_label=show_label,
                                    show_rules=show_rules,
                                    depth=depth + 1,
                                    is_primitive=is_primitive) + "\n"
            else:
                result += formatter(data=value,
                                    show_label=show_label,
                                    show_rules=show_rules,
                                    depth=depth,
                                    is_primitive=is_primitive)
                result += '\n'
                result += parse(data=value.get('type'),
                                show_label=show_label,
                                show_secret=show_secret,
                                show_rules=show_rules,
                                depth=depth + 1)
    return result


if __name__ == "__main__":
    show_label = True
    show_secret = True
    show_rules = True
    parsed_data = parse(data=config.__metadata__(),
                        show_label=show_label,
                        show_secret=show_secret,
                        show_rules=show_rules)
    print(parsed_data)
    open("out.txt", 'w').write(parsed_data)
