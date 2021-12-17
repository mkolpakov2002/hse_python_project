import os
import pandas as pd


def initialize_dir(way):
    """
    Автор: Максим Колпаков
    -----------------------
    Выбор директории для хранения проекта
    Параметры
    ----------
    way : str
          название основной папки
    Возвращает
    -------
    None
    """
    os.getcwd()
    os.chdir(way)


def initialize_data(way):
    """
    Автор: Максим Колпаков
    -----------------------
    Выбор файла с базой данных
    Параметры
    ----------
    way : str
          название файла с данными
    Возвращает
    -------
    Data : pandas.core.frame.DataFrame
           основная база данных
    """
    assert os.path.isfile(way)
    check_for_line_break(way)
    DATA = pd.read_csv(way, delimiter=',', encoding='utf-8')
    return DATA


def check_for_line_break(way):
    """
    Автор: Максим Колпаков
    -----------------------
    Проверка на наличие '/n' в файле с базой данных
    Параметры
    ----------
    way : str
         название папки/файла
    Возвращает
    -------
    None
    """
    with open(way, 'r', encoding='utf-8') as file:
        data = file.readlines()
        last_row = data[-1]
        last_char = last_row[-1]
        if last_char != '\n':
            append_line_break(way)


def append_line_break(way):
    """
    Автор: Максим Колпаков
    -----------------------
    Добавление '/n' в файл с базой данных для корректного чтения данных
    Параметры
    ----------
    way : str
          название основной папки
    Data : pandas.core.frame.DataFrame
           основная база данных
    Возвращает
    -------
    None
    """
    with open(way, 'a', encoding='utf-8') as f_d:
        f_d.write('\n')
