# Metadata Parser
## Описание
Предназначен для парсинга `__metadata__()` параметрики.
Выводит значения полей и их описания (опционально), что позволяет прочитать данные конфигурации.
Записывает значения полей в файле `out.txt`.

## Установка
1. Скачать репозиторий `git clone https://github.com/Demono5060/Metadata_parser.git`
2. Установить зависимости `pip3 install -r requirements.txt`
3. Запустить приложение `python3 main.py`

---
Обратите внимание, что для того, чтобы скрипт отработал корректно,
файл описывающий конфигурацию должен иметь название `config.py`.
`Пример содержимого такого файла вы можете найти в этом репозитории под названием config.py.`
Название основного объекта конфигурации должно быть `config`.
`Пример объекта вы можете найти внутри файла config.py, расположенного в данном репозитории.`
---

## Настройка опций
##### Доступные опции
Текущий скрипт поддерживает несколько опциональных возможностей (по стандарту выключены все),
включаются они при добавлении соответствующих флагов к скрипту.
Пример использования опций: `python3 main.py -ss -show-rules -sh -o filename.txt`
1. `-sh` или `--show-hint` - отвечает за отображение описаний полей.
2. `-ss` или `--show-secret` - отвечает за отображение секретных полей.
3. `-sr` или `--show-rules` - отвечает за отображение правил (возможных значений полей).
4. `-p` или `--primitive` - включить отображение только примитивных полей.
5. `-o OUT` или `--out OUT` - при добавлении этого флага вам будет необходимо указать файл, который будет использован для записи вывода.