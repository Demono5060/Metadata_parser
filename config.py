from enum import Enum
from uuid import uuid4
from datetime import datetime
from random import randint
from typing import List, Tuple

from ext.parametrica import Fieldset, Field, InRange, Min, Parametrica, Max, Match
from ext.parametrica.io import YAMLFileConfigIO, VirtualYAMLFileConfigIO
from ext.parametrica.predefined.network import HTTPServer, Credentials, PortField


class MyEnum(Enum):

    VALUE1 = 'value1'
    VALUE2 = 'value2'
    VALUE3 = 'value3'


class Common(Fieldset):

    int_field = Field[int](220).label('Интовое поле').hint('Записывается сюда какое-то значение целочисленное')
    flag = Field[bool](False).label('Флаг значение').hint('Тут понятно должно быть что оно в себе хранит')
    string = Field[str]('STR').label('Строчный тип типа').hint('Используется для хранения строки')
    enum_field = Field[MyEnum](MyEnum.VALUE2).label('Тут хранится enum')
    list_field = Field[List[int]]([1, 2, 3, 4,]).label('Списочек')
    empty_list = Field[List[int]]().label('Пустой списочек')
    tuple_field = Field[Tuple[bool]]((False, True, True)).label('Кортеж')
    empty_tuple = Field[Tuple[bool]]().label('Пустой кортеж')


class Lvl1(Fieldset):

    class Lvl2(Fieldset):

        class Lvl3(Fieldset):

            class Lvl4(Fieldset):
                
                class Lvl5(Fieldset):

                    class Lvl6(Fieldset):

                        click_me = Field[str]('https://www.youtube.com/watch?v=dQw4w9WgXcQ').label('Нажми на меня')
                    
                    lvl6 = Field[Lvl6]().label('lvl6')

                lvl5 = Field[Lvl5]().label('lvl5')

            lvl4 = Field[Lvl4]().label('lvl4')
            
        lvl3 = Field[Lvl3]().label('lvl3')

    lvl2 = Field[Lvl2]().label('lvl2')
    

class ServerData(HTTPServer, Credentials):
    ...


class MoreFields(Fieldset):

    empty = Field[int](0)
    label = Field[int](1).label('Some label')
    hint = Field[int](2).hint('Some hint')
    secret = Field[str]('SECRET').secret()
    rule_range = Field[int](4).rule(InRange(0, 30)).label('0-30')
    rule_min = Field[int](10).rule(Min(5)).label('min 5')
    rule_max = Field[int](5).rule(Max(15)).label('max 15')
    email = Field[str]('some_email@gmail.com').label('Email адрес').rule(Match(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)'))
    secret_token = Field[str](uuid4).label('Супер секретный токен').hint('Его нигде и ниеогда не палить').secret()
    default = Field[int](1).default(lambda: 100 * randint(1, 60))
    port = PortField(3000)


class CustomDefaultVal(Fieldset):

    default_1234 = Field[int](1234).label('Тут должно было быть 1234')


class Config(Parametrica):

    common = Field[Common]().label('Общие поля для примера').hint('Сюда вписывать примитивы')
    lvl1 = Field[Lvl1]().label('lvl1')
    more_fields = Field[MoreFields]().label('Абсолютно разношерстные поля')
    server_field = Field[ServerData]().label('Данные для подключения к серверу')
    created_time = Field[str](datetime.now().isoformat).label('Время создания конфига')
    custom_default = Field[str]('CustomDefault').label('Кастомное дефолт значение 1, которое никогда не появится')
    custom_default_1 = Field[CustomDefaultVal](CustomDefaultVal(default_1234=1111)).label('Кастомное дефолт значение 1')
    custom_default_2 = Field[CustomDefaultVal](default_1234=2222).label('Кастомное дефолт значение 2')


class DevEnv(Parametrica):

    is_dev = Field[bool](False).label('Использовать окружение разработчика')


config = Config(YAMLFileConfigIO('settings.yaml'))
dev_env = DevEnv(VirtualYAMLFileConfigIO('dev.env'))
