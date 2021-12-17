from tkinter import ttk
from pathlib import Path
import tkinter as tki
import csv
import sys
import numpy as np
import pandas as pd
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
sys.path.append(str(Path().absolute().parent/'Library'))
from init_data_and_base import initialize_dir, initialize_data
from select_ways import choose_the_way, WAYS
matplotlib.use('TkAgg')


def initialize_main_window():
    """
    Автор: Максим Колпаков
    -----------------------
    Создание главного окна приложения win_main
    Возвращает
    -------
    None
    """
    initialize_dir(DIRECTORY_WAY)
    initialize_dir(GRAPH_WAY)
    global DATA
    DATA = initialize_data(BASE_WAY)
    global WIN_MAIN
    WIN_MAIN = Window()
    frame_for_data_operations = tki.Frame(WIN_MAIN)
    frame_for_data_operations.pack()
    label_buttons = tki.Label(frame_for_data_operations,
                              text="Действия над таблицей", font="Arial 9")
    label_buttons.pack(side=tki.TOP)
    button_add = tki.Button(frame_for_data_operations, text="Добавить",
                            width=10, height=1, command=add)
    button_add.pack(side=tki.LEFT, padx=10, pady=10)
    button_sort = tki.Button(frame_for_data_operations, text="Сортировать",
                             width=10, height=1, command=sort_by)
    button_sort.pack(side=tki.LEFT, padx=10, pady=10)

    def delete_items_from_tree():
        """
        Автор: Максим Колпаков
        -----------------------
        Удаление выбранных строк из базы данных,
        сохранение обновленной базы в csv файл
        Возвращает
        -------
        None
        """
        global DATA
        if WIN_MAIN.main_obj.selected_number > 0:
            for selected_item in WIN_MAIN.main_obj.tree.selection():
                children = list(map(int,
                                    WIN_MAIN.main_obj.tree.get_children()))
                for iid in children:
                    if (WIN_MAIN.main_obj.tree.item(iid)['text'] ==
                            WIN_MAIN.main_obj.tree.item(
                                selected_item, "text")):
                        DATA = DATA.drop(DATA.index[children.index(iid)])
                        break
                WIN_MAIN.main_obj.tree.delete(selected_item)
                WIN_MAIN.main_obj.base_length -= 1
            DATA.to_csv(BASE_WAY, sep=",", index=False)

    button_delete = tki.Button(frame_for_data_operations, text="Удалить",
                               width=10, height=1,
                               command=delete_items_from_tree)
    button_delete.pack(side=tki.LEFT, padx=10, pady=10)

    def check_selected_and_change():
        """
        Автор: Максим Колпаков
        -----------------------
        Получение порядкового номера и id выбранной строки,
        вызов функции для её изменения
        Возвращает
        -------
        None
        """
        if len(WIN_MAIN.main_obj.tree.selection()) == 1:
            position = -1
            id_of_row = -1
            selected_item = WIN_MAIN.main_obj.tree.selection()[0]
            children = list(map(int, WIN_MAIN.main_obj.tree.get_children()))
            for iid in children:
                if (WIN_MAIN.main_obj.tree.item(iid)['text'] ==
                        WIN_MAIN.main_obj.tree.item(selected_item, "text")):
                    position = children.index(iid)
                    id_of_row = WIN_MAIN.main_obj.tree.item(iid)['text']
                    break
            change(position, id_of_row)
        else:
            tki.messagebox.showinfo(
                "Ошибка", "Одновременно изменять можно ровно одну строку")
    button_change = tki.Button(frame_for_data_operations,
                               text="Изменить",
                               width=10,
                               height=1,
                               command=check_selected_and_change)
    button_change.pack(side=tki.LEFT, padx=10, pady=10)
    frame_for_plots = tki.LabelFrame(
        WIN_MAIN, text="Анализ профессий в графиках")
    frame_for_plots.pack()
    combo_choose_plot = ttk.Combobox(
        frame_for_plots,
        state="readonly",
        width=60,
        values=['Кол-во профессий по специализациям',
                'Зависимость средней зарплаты от специализации',
                'Распределение количества вакансий от зп. в городе',
                'Кол-во вакансий по специализациям в зависимости от города',
                'Кол-во очных и дистанционных вакансий по специализациям'])
    combo_choose_plot.current(0)
    combo_choose_plot.pack()

    def check_selected():
        """
        Автор: Татьяна Рыкова
        -----------------------
        Вызов функции построения графика по нажатии на кнопку Построить
        Возвращает
        -------
        None
        """
        construct(combo_choose_plot.get())

    button_city_money = tki.Button(frame_for_plots, text="Построить",
                                   width=10, height=1, command=check_selected)
    button_city_money.pack()

    btn_exit = tki.Button(WIN_MAIN, text='Выход', height=1,
                          command=WIN_MAIN.destroy, cursor='hand2')
    btn_exit.pack()
    WIN_MAIN.mainloop()


# первый график
def first(data):
    """
    Автор: Татьяна Рыкова
    -----------------------
    График количества профессий по специализациям

    Параметры
    ----------
    data : pandas.core.frame.DataFrame
           база данных из csv файла

    Возвращает
    -------
    current_figure : matplotlib.figure.Figure
            построенный график

    """
    labels = list(np.unique(data['Специализация']))
    row_count = len(data)
    offers_number_list = []
    procent_list = []
    labels_plot = []
    for i in range(len(labels)):
        offers_number_list.insert(
            i,
            (data['Специализация'] == f'{labels[i]}').sum()
        )
        procent_list.insert(i, offers_number_list[i] * 100 / row_count)
        labels_plot.insert(i, f'{labels[i]} ({round(procent_list[i], 2)}%)')
    current_figure = Figure(figsize=(12, 6))
    current_plot = current_figure.add_subplot()
    current_plot.pie(offers_number_list, labels=labels_plot)
    current_plot.set_title(
        f'Всего доступно {row_count} вакансий',
        fontdict={'size': 20}
    )
    current_plot.axis('equal')
    way = GRAPH_WAY + "/first_graph.png"
    current_figure.savefig(f"{way}")
    tki.messagebox.showinfo("Информация", f"График сохранён в {way}")
    return current_figure


# второй график
def second(data):
    """
    Автор: Татьяна Рыкова
    -----------------------
    График зависимости средней зарплаты от специализации
    Параметры
    ----------
    data : pandas.core.frame.DataFrame
           база данных из csv файла
    Возвращает
    -------
    current_figure : matplotlib.figure.Figure
            построенный график
    """
    salary_list = []
    labels = list(np.unique(data['Специализация']))
    for i in range(len(labels)):
        salary_list.insert(
            i,
            data.loc[
                data['Специализация'] == f'{labels[i]}', 'Зарплата'].mean()
        )
    current_figure = Figure(figsize=(7, 9))
    current_plot = current_figure.add_subplot()

    current_plot.set_title('Зависимость средней зарплаты от специализации')
    current_plot.bar(labels, salary_list)
    current_plot.set_xticks(labels)
    current_plot.set_xticklabels(
        labels, horizontalalignment='right', rotation=45, size=12)
    current_plot.set_facecolor('seashell')
    current_plot.yaxis.grid()
    current_figure.subplots_adjust(bottom=0.31)
    way = GRAPH_WAY + "/second_graph.png"
    current_figure.savefig(f"{way}")
    tki.messagebox.showinfo("Информация", f"График сохранён в {way}")
    return current_figure


# третий график
def third(selected):
    """
    Автор: Владислав Огай
    -----------------------
    График распределения количества вакансий от зп. в городе
    Параметры
    ----------
    selected : str
                название выбранного пользователем города из comboExample
    Возвращает
    -------
    current_figure : matplotlib.figure.Figure
            построенный график
    """
    salary_list_int = DATA.loc[DATA['Город'] == selected, 'Зарплата'].values
    current_figure = Figure(figsize=(6, 6))
    current_plot = current_figure.add_subplot()
    current_plot_histogram = current_plot.hist(x=salary_list_int, bins=10)[0]
    current_plot.grid(axis='y', alpha=0.75)
    current_plot.set_xlabel('Зарплата, тыс. руб.')
    current_plot.set_ylabel('Кол-во вакансий')
    current_plot.set_title(
        'Распределение количества вакансий от зп. в городе ' + selected)
    maxfreq = current_plot_histogram.max()
    current_plot.set_ylim(
        ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    way = GRAPH_WAY + "/third_graph.png"
    current_figure.savefig(way)
    tki.messagebox.showinfo("Информация", f"График сохранён в {way}")
    make_window_plot(current_figure)

# четвертый график


def fourth(data):
    """
    Автор: Владислав Огай
    -----------------------
    График по количеству вакансий в специализациях в зависимости от города
    Параметры
    ----------
    data : pandas.core.frame.DataFrame
           база данных из csv файла
    Возвращает
    -------
    current_figure : matplotlib.figure.Figure
            построенный график
    """
    way = GRAPH_WAY + "/fourth_graph.png"
    tki.messagebox.showinfo("Информация", f"График сохранён в {way}")
    current_figure = plt.figure(figsize=(6, 8))
    current_plot = current_figure.add_subplot()
    labels = list(np.unique(data['Специализация']))
    list_offers_number_moscow = []
    list_offers_number_leningrad = []
    list_offers_number_kazan = []
    list_offers_number_other = []
    for i in range(len(labels)):
        list_offers_number_moscow.insert(
            i,
            ((data['Специализация'] == f'{labels[i]}') &
             (data['Город'] == 'Москва')).sum()
        )
        list_offers_number_leningrad.insert(
            i,
            ((data['Специализация'] == f'{labels[i]}') &
             (data['Город'] == 'Санкт-Петербург')).sum()
        )
        list_offers_number_kazan.insert(
            i,
            ((data['Специализация'] == f'{labels[i]}') &
             (data['Город'] == 'Казань')).sum()
        )
        list_offers_number_other.insert(
            i,
            ((data['Специализация'] == f'{labels[i]}') &
             (data['Город'] != 'Москва') &
             (data['Город'] != 'Санкт-Петербург') &
             (data['Город'] != 'Казань')).sum()
        )  # / (len(town) - 3))
    m_1 = max(len(list_offers_number_moscow),
              len(list_offers_number_leningrad))
    m_2 = max(len(list_offers_number_kazan),
              len(list_offers_number_other))
    m_3 = max(m_1, m_2)  # макс колво запросов
    data_plot = {'Москва': list_offers_number_moscow,
                 'Санкт-Петербург': list_offers_number_leningrad,
                 'Казань': list_offers_number_kazan,
                 'Остальные города': list_offers_number_other}

    d_f = pd.DataFrame(data_plot)
    d_f.plot(kind='bar', ax=current_plot)
    current_plot.set_title(
        'Количество вакансий по специализациям \n в зависимости от города',
        size=12)
    current_plot.set_xticklabels(
        labels, horizontalalignment='right', rotation=45, size=9)
    current_plot.set_yticks([i for i in range(m_3 + 1)])
    current_figure.subplots_adjust(bottom=0.31)
    current_figure.savefig(f"{way}")
    return current_figure


# пятый график
def fifth(data):
    """
    Автор: Максим Колпаков
    -----------------------
    График по количеству очных и дистанционных вакансий по специализациям
    Параметры
    ----------
    data : pandas.core.frame.DataFrame
           база данных из csv файла
    Возвращает
    -------
    current_figure : matplotlib.figure.Figure
            построенный график
    """
    way = GRAPH_WAY + "/fifth_graph.png"
    tki.messagebox.showinfo("Информация", f"График сохранён в {way}")
    current_figure = plt.figure(figsize=(6, 8))
    current_plot = current_figure.add_subplot()
    labels = list(np.unique(data['Специализация']))
    list_offers_number_full_time = []
    list_offers_number__distant = []
    for i in range(len(labels)):
        list_offers_number_full_time.insert(
            i,
            ((data['Специализация'] == f'{labels[i]}') &
             (data['Тип занятости'] == 'Очная')).sum()
        )
        list_offers_number__distant.insert(
            i,
            ((data['Специализация'] == f'{labels[i]}') &
             (data['Тип занятости'] == 'Удаленная')).sum()
        )
    data = {'Очно': list_offers_number_full_time,
            'Дистанционно': list_offers_number__distant}
    d_f = pd.DataFrame(data)
    d_f.plot(kind='bar', stacked=True, ax=current_plot)
    current_plot.set_title(
        'Количество очных и дистанционных вакансий \n по специализациям')
    current_plot.set_xticklabels(
        labels, rotation=60, horizontalalignment='right')
    current_figure.subplots_adjust(bottom=0.36)
    current_figure.savefig(f"{way}")
    return current_figure


class MakeTable(object):
    """
    Автор: Владислав Огай
    -----------------------
    Класс для создания сводной таблицы
    Атрибуты
    ----------
     way : str
          название файла с базой данных
     length : str
          количество столбцов в таблице
     app : str
          название ttk.Treeview окна
     code : str
          название кодировки (в проекте 'utf-8')
    Методы
    -------
    number_of_selected(event)
    delete_items_from_tree()
    """

    def __init__(self, way, length, app, code):
        """
        Автор: Владислав Огай
        -----------------------
        Устанавливает все необходимые атрибуты для объекта MakeTable
        Параметры
        ----------
        way : str
              название файла с базой данных
        length : str
              количество столбцов в таблице
        app : str
              название ttk.Treeview окна
        code : str
              название кодировки
        """
        i = 0
        self.selected_number = -1
        self.way = way
        with open(way, 'r', encoding=code) as f_1:
            reader = csv.reader(f_1, delimiter=',')
            row1 = next(reader)
            columns_from_table = list(row1)
            length = len(columns_from_table)
            columns_default = []
            for i in range(length):
                columns_default.append(f"#{i+1}")
            scrollbar = ttk.Scrollbar(app)

            self.tree = ttk.Treeview(app, padding=3, show="headings",
                                     columns=columns_default,
                                     yscrollcommand=scrollbar.set)
            scrollbar.config(command=self.tree.yview)
            scrollbar.pack(side=tki.RIGHT, fill=tki.Y)
            i = 0
            for i in range(length):
                self.tree.heading(
                    columns_default[i], text=columns_from_table[i])
            i = 0
            self.base_length = 0
        with open(way, 'r', encoding=code) as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                i = i + 1
                if i != 1:
                    self.tree.insert("", 'end', iid=i-2, text=i-2, values=row)
                    self.base_length = self.base_length + 1
                if i == 2:
                    self.tree.bind("<<TreeviewSelect>>",
                                   self.number_of_selected)

    def number_of_selected(self, event):
        """
        Автор: Владислав Огай
        -----------------------
        Считает количество элементов, выбранных для удаления
        """
        self.selected_number = len(self.tree.selection())


def add():  # добавление данных
    """
    Автор: Максим Колпаков
    -----------------------
    Обработка нажатия кнопки Добавить
    """
    win_new = tki.Toplevel()
    win_new.title("Добавление")
    frame_for_input = tki.Frame(win_new)
    frame_for_buttons = tki.Frame(win_new)
    btn_exit = tki.Button(frame_for_buttons, text='Выход',
                          command=win_new.destroy, cursor='hand2')
    frame_for_input.pack()
    label_1 = tki.Label(frame_for_input, text="Количество добавляемых строк: ")
    label_1.pack(side=tki.LEFT, padx=10, pady=10)
    entry_1 = tki.Entry(frame_for_input, width=4)
    entry_1.pack(side=tki.LEFT, padx=10, pady=10)

    def input_data():
        """
        Автор: Татьяна Рыкова
        -----------------------
        Ввод новых данных и проверка их на корректность
        """
        flag = False
        size = 0
        try:
            size = int(entry_1.get())
            if size <= 0:
                flag = True
        except ValueError:
            flag = True
        if flag:
            entry_1.delete(0, 'end')
            tki.messagebox.showinfo(
                "Ошибка", "Проверьте правильность введённых данных")
        elif int(entry_1.get()) > 20:
            tki.messagebox.showinfo(
                "Информация", "Одновременно можно добавлять не более 20 строк")
        else:
            def update_table():  # сворачивание окон
                """
                Автор: Максим Колпаков
                -----------------------
                Обновление базы данных
                """
                flag = False
                for i in range(kol_rows-1):
                    try:
                        int(code_list[i].get())
                    except ValueError:
                        flag = True
                        code_list[i].delete(0, 'end')
                    try:
                        salary = int(salary_list[i].get())
                        if salary <= 0:
                            flag = True
                            salary_list[i].delete(0, 'end')
                    except ValueError:
                        flag = True
                        salary_list[i].delete(0, 'end')
                if not flag:
                    buffer_list = []
                    way = BASE_WAY
                    for i in range(kol_rows-1):
                        buffer = []
                        buffer.append(code_list[i].get())
                        buffer.append(spec_list[i].get())
                        buffer.append(prof_list[i].get())
                        buffer.append(work_type_list[i].get())
                        buffer.append(town_list[i].get())
                        buffer.append(salary_list[i].get())
                        buffer.append(year_working_list[i].get())
                        buffer_list.append(buffer)
                    last_el = list(
                        map(int, WIN_MAIN.main_obj.tree.get_children()))[-1]
                    with open(way,
                              "a+",
                              newline='\n',
                              encoding='utf-8') as file:
                        writer = csv.writer(file, delimiter=',')
                        for i in range(kol_rows-1):
                            writer.writerow(buffer_list[i])
                            WIN_MAIN.main_obj.tree.insert(
                                '', 'end', iid=last_el+1+i,
                                text=last_el+1+i, values=buffer_list[i])
                            WIN_MAIN.main_obj.base_length += 1
                    global DATA
                    DATA = initialize_data(BASE_WAY)
                    win_new_next.destroy()
                    tki.messagebox.showinfo(
                        "Информация", "База данных обновлена")
                else:
                    tki.messagebox.showinfo(
                        "Ошибка", "Проверьте правильность введённых данных")
            kol_rows = int(entry_1.get()) + 1
            win_new.destroy()
            win_new_next = tki.Tk()
            win_new_next.title("Внесение данных")
            win_new_next.geometry("930x500")
            # --- create canvas with scrollbar ---
            frame_for_table_and_scroll = tki.LabelFrame(
                win_new_next, text="Внесение данных")
            canvas = tki.Canvas(frame_for_table_and_scroll)
            frame = tki.Frame(canvas)
            scrollbar = tki.Scrollbar(
                frame_for_table_and_scroll, command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side=tki.LEFT, fill=tki.BOTH, expand=True)
            scrollbar.pack(side=tki.RIGHT, fill=tki.BOTH)
            frame.pack(fill=tki.BOTH, expand=True)

            def on_frame_configure(event):
                """
                Автор: Владислав Огай
                -----------------------
                Вывод сводной таблицы в отдельном окне
                """
                canvas.configure(scrollregion=frame.bbox('all'))

            def on_canvas_configure(event):
                """
                Автор: Владислав Огай
                -----------------------
                Вывод сводной таблицы
                """
                canvas.itemconfigure(_frame_id, width=canvas.winfo_width())
            _frame_id = canvas.create_window(
                canvas.winfo_width(), 0,
                anchor='nw',
                window=frame)
            frame.bind('<Configure>', on_frame_configure)
            canvas.bind('<Configure>', on_canvas_configure)
            width = 7
            label_list = []
            label_list.append(tki.Label(frame, text="Код"))
            label_list.append(tki.Label(frame, text="Специализация"))
            label_list.append(tki.Label(frame, text="Профессия"))
            label_list.append(tki.Label(frame, text="Тип занятости"))
            label_list.append(tki.Label(frame, text="Город"))
            label_list.append(tki.Label(frame, text="Зарплата"))
            label_list.append(tki.Label(frame, text="Опыт работы"))
            # Массивы для полей вводимых данных
            code_list = []
            spec_list = []
            prof_list = []
            work_type_list = []
            town_list = []
            salary_list = []
            year_working_list = []
            for i in range(kol_rows):  # Rows
                for j in range(width):  # Columns
                    if i == 0:
                        label_list[j].grid(row=i, column=j)
                    else:
                        if j == 0:
                            code_list.append(tki.Entry(frame, text=""))
                            code_list[i-1].grid(row=i, column=j)
                        elif j == 1:
                            spec_list.append(tki.Entry(frame, text=""))
                            spec_list[i-1].grid(row=i, column=j)
                        elif j == 2:
                            prof_list.append(tki.Entry(frame, text=""))
                            prof_list[i-1].grid(row=i, column=j)
                        elif j == 3:
                            work_type_list.append(ttk.Combobox(
                                frame, state="readonly",
                                values=['Очная', 'Удаленная']))
                            work_type_list[i-1].current(0)
                            work_type_list[i-1].grid(row=i, column=j)
                        elif j == 4:
                            town_list.append(tki.Entry(frame, text=""))
                            town_list[i-1].grid(row=i, column=j)
                        elif j == 5:
                            salary_list.append(tki.Entry(frame, text=""))
                            salary_list[i-1].grid(row=i, column=j)
                        elif j == 6:
                            year_working_list.append(
                                ttk.Combobox(frame, state="readonly",
                                             values=['менее 1 года',
                                                     '1-2 года',
                                                     '3-4 года',
                                                     'более 5 лет']))
                            year_working_list[i-1].current(0)
                            year_working_list[i-1].grid(row=i, column=j)
            frame_for_table_and_scroll.pack(expand=True, fill=tki.BOTH)
            button_update = tki.Button(
                win_new_next,
                text="Обновить базу данных",
                height=1,
                command=update_table)
            button_update.pack(side=tki.BOTTOM)
            button_exit = tki.Button(
                win_new_next,
                text='Выход',
                height=1,
                command=win_new_next.destroy,
                cursor='hand2')
            button_exit.pack(side=tki.BOTTOM)
            win_new_next.mainloop()
    button_input = tki.Button(frame_for_buttons, text="Ок", command=input_data)
    frame_for_buttons.pack()
    btn_exit.pack(side=tki.LEFT, padx=10, pady=10)
    button_input.pack(side=tki.LEFT, padx=10, pady=10)
    win_new.mainloop()


def change(position, id_of_row):
    """
    Автор: Максим Колпаков
    -----------------------
    Изменение одной строки базы данных
    """
    def update_table():
        """
        Автор: Максим Колпаков
        -----------------------
        Обновление базы данных
        """
        flag = False
        try:
            int(code_entry.get())
        except ValueError:
            flag = True
            code_entry.delete(0, 'end')
        try:
            salary = int(salary_entry.get())
            if salary <= 0:
                flag = True
                salary_entry.delete(0, 'end')
        except ValueError:
            flag = True
            salary_entry.delete(0, 'end')
        if not flag:
            buffer = []
            buffer.append(code_entry.get())
            buffer.append(spec_entry.get())
            buffer.append(prof_entry.get())
            buffer.append(work_type_entry.get())
            buffer.append(town_entry.get())
            buffer.append(salary_entry.get())
            buffer.append(year_working_entry.get())
            DATA.loc[position] = buffer
            DATA.to_csv(BASE_WAY, sep=",", index=False)
            WIN_MAIN.main_obj.tree.item(id_of_row, values=buffer)
            win_new_next.destroy()
            tki.messagebox.showinfo("Информация", "База данных обновлена")
        else:
            tki.messagebox.showinfo(
                "Ошибка", "Проверьте правильность введённых данных")
    kol_rows = 2
    win_new_next = tki.Tk()
    win_new_next.title("Изменение базы данных")
    win_new_next.geometry("930x500")
    # --- create canvas with scrollbar ---
    frame_for_table_and_scroll = tki.LabelFrame(
        win_new_next, text="Изменение данных")

    canvas = tki.Canvas(frame_for_table_and_scroll)
    frame = tki.Frame(canvas)
    scrollbar = tki.Scrollbar(frame_for_table_and_scroll, command=canvas.yview)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=tki.LEFT, fill=tki.BOTH, expand=True)
    scrollbar.pack(side=tki.RIGHT, fill=tki.BOTH)
    frame.pack(fill=tki.BOTH, expand=True)

    def on_frame_configure(event):
        """
        Автор: Владислав Огай
        -----------------------
        Вывод сводной таблицы в отдельном окне
        """
        canvas.configure(scrollregion=frame.bbox('all'))

    def on_canvas_configure(event):
        """
        Автор: Владислав Огай
        -----------------------
        Вывод сводной таблицы
        """
        canvas.itemconfigure(_frame_id, width=canvas.winfo_width())
    _frame_id = canvas.create_window(
        canvas.winfo_width(), 0,
        anchor='nw',
        window=frame)
    frame.bind('<Configure>', on_frame_configure)
    canvas.bind('<Configure>', on_canvas_configure)
    width = 7
    label_list = []
    label_list.append(tki.Label(frame, text="Код"))
    label_list.append(tki.Label(frame, text="Специализация"))
    label_list.append(tki.Label(frame, text="Профессия"))
    label_list.append(tki.Label(frame, text="Тип занятости"))
    label_list.append(tki.Label(frame, text="Город"))
    label_list.append(tki.Label(frame, text="Зарплата"))
    label_list.append(tki.Label(frame, text="Опыт работы"))
    for i in range(kol_rows):  # Rows
        for j in range(width):  # Columns
            if i == 0:
                label_list[j].grid(row=i, column=j)
            else:
                if j == 0:
                    code_entry = tki.Entry(frame)
                    code_entry.insert(0, DATA.values[position][j])
                    code_entry.grid(row=i, column=j)
                elif j == 1:
                    spec_entry = (tki.Entry(frame))
                    spec_entry.insert(0, DATA.values[position][j])
                    spec_entry.grid(row=i, column=j)
                elif j == 2:
                    prof_entry = (tki.Entry(frame))
                    prof_entry.insert(0, DATA.values[position][j])
                    prof_entry.grid(row=i, column=j)
                elif j == 3:
                    work_type_entry = (ttk.Combobox(
                        frame, state="readonly",
                        values=['Очная', 'Удаленная']))
                    if DATA.values[position][j] == 'Очная':
                        work_type_entry.current(0)
                    else:
                        work_type_entry.current(1)
                    work_type_entry.grid(row=i, column=j)
                elif j == 4:
                    town_entry = (tki.Entry(frame))
                    town_entry.insert(0, DATA.values[position][j])
                    town_entry.grid(row=i, column=j)
                elif j == 5:
                    salary_entry = (tki.Entry(frame))
                    salary_entry.insert(0, DATA.values[position][j])
                    salary_entry.grid(row=i, column=j)
                elif j == 6:
                    year_working_entry = (ttk.Combobox(
                        frame, state="readonly",
                        values=['менее 1 года',
                                '1-2 года',
                                '3-4 года',
                                'более 5 лет']))
                    if DATA.values[position][j] == 'менее 1 года':
                        year_working_entry.current(0)
                    elif DATA.values[position][j] == '1-2 года':
                        year_working_entry.current(1)
                    elif DATA.values[position][j] == '3-4 года':
                        year_working_entry.current(2)
                    elif DATA.values[position][j] == 'более 5 лет':
                        year_working_entry.current(3)
                    year_working_entry.grid(row=i, column=j)
    frame_for_table_and_scroll.pack(expand=True, fill=tki.BOTH)
    button_update = tki.Button(
        win_new_next,
        text="Обновить базу данных",
        height=1,
        command=update_table)
    button_update.pack(side=tki.BOTTOM)
    button_exit = tki.Button(
        win_new_next,
        text='Выход',
        height=1,
        command=win_new_next.destroy,
        cursor='hand2')
    button_exit.pack(side=tki.BOTTOM)
    win_new_next.mainloop()


def sort_by():
    """
    Автор: Татьяна Рыкова
    -----------------------
    Обработка нажатия кнопки Сортировка
    """
    win_new = tki.Tk()
    win_new.title("Сортировка")
    win_new.geometry("400x300+450+250")
    btn_exit = tki.Button(
        win_new,
        text='Выход',
        font=('Arial', 15),
        bg='grey',
        fg='yellow',
        height=1,
        width=10,
        command=win_new.destroy,
        cursor='hand2')
    btn_exit.pack(side="bottom")
    label_1 = tki.Label(win_new, text="Сортировать по ")
    label_1.place(relx=.1, rely=.1)
    combo_example = ttk.Combobox(
        win_new,
        state="readonly",
        width=30,
        values=['ср. зп. по спец. в городах',
                'убыванию зарплат',
                'возрастанию зарплат',
                'количеству профессий в спец.',
                'ср. зп. по спец.'])
    combo_example.current(0)
    combo_example.place(relx=.4, rely=.1)

    def choose_sort():
        """
        Автор: Владислав Огай
        -----------------------
        Выбор вида сортировки из ComboBox
        Возвращает
        -------
        Измененную/новую сводную таблицу, сохраненную в csv файл
        """
        if combo_example.get() == 'количеству профессий в спец.':
            tki.messagebox.showinfo(
                "Информация",
                "Отсортированный файл сохранён в Output/table1.csv")
            # update tabControl
            win_table = tki.Toplevel(WIN_MAIN)
            length = 0
            frame_tabels = ttk.LabelFrame(
                win_table, text='Сортировка по ' + combo_example.get())
            # Первая таблица
            num_1 = pd.crosstab(
                DATA["Специализация"], "Количество профессий").reset_index()
            way = DIRECTORY_WAY + "/Output/table1.csv"
            num_1.to_csv(f"{way}", sep=",", index=False)
            main_obj = MakeTable(way, length, frame_tabels, 'utf-8')
            main_tree = main_obj.tree
            main_tree.pack(side=tki.BOTTOM, fill=tki.BOTH, expand=tki.YES)
            frame_tabels.pack()  # положение
            win_new.destroy()
            win_table.mainloop()
        elif combo_example.get() == 'ср. зп. по спец.':
            tki.messagebox.showinfo(
                "Информация",
                "Отсортированный файл сохранён в Output/table2.csv")
            win_table = tki.Toplevel(WIN_MAIN)
            length = 0
            frame_tabels = ttk.LabelFrame(
                win_table, text='Сортировка по ' + combo_example.get())
            num_2 = pd.pivot_table(DATA, index=["Специализация"], values=[
                                  "Зарплата"], aggfunc="mean")
            num_2 = num_2['Зарплата'].round().astype(int)
            way = DIRECTORY_WAY + "/Output/table2.csv"
            num_2 = num_2.to_frame().reset_index()
            num_2.to_csv(f"{way}", sep=",", index=False)
            main_obj = MakeTable(way, length, frame_tabels, 'utf-8')
            main_tree = main_obj.tree
            main_tree.pack(side=tki.BOTTOM, fill=tki.BOTH, expand=tki.YES)
            frame_tabels.pack()  # положение
            win_new.destroy()
            win_table.mainloop()
        elif combo_example.get() == 'ср. зп. по спец. в городах':
            tki.messagebox.showinfo(
                "Информация",
                "Отсортированный файл сохранён в Output/table3.csv")
            win_table = tki.Toplevel(WIN_MAIN)
            length = 0
            frame_tabels = ttk.LabelFrame(
                win_table, text='Сортировка по ' + combo_example.get())
            num_3 = pd.pivot_table(DATA, index=["Профессия", "Город"], values=[
                                  "Зарплата"]).reset_index()
            way = DIRECTORY_WAY + "/Output/table3.csv"
            num_3.to_csv(f"{way}", sep=",", index=False)
            main_obj = MakeTable(way, length, frame_tabels, 'utf-8')
            main_tree = main_obj.tree
            main_tree.pack(side=tki.BOTTOM, fill=tki.BOTH, expand=tki.YES)
            frame_tabels.pack()  # положение
            win_new.destroy()
            win_table.mainloop()
        else:
            length = 0
            win_table = tki.Toplevel(WIN_MAIN)
            frame_tabels = ttk.LabelFrame(
                win_table, text='Сортировка по ' + combo_example.get())
            if combo_example.get() == 'убыванию зарплат':
                data_sorted = DATA.sort_values(
                    by='Зарплата', ascending=False)
                tki.messagebox.showinfo(
                    "Информация", "Отсортированный файл сохранён \
                        в Output/Data_sorted_in_descending_order.csv")
                way = (DIRECTORY_WAY +
                       "/Output/Data_sorted_in_descending_order.csv")
                data_sorted.to_csv(f"{way}", sep=",", index=False)
            else:
                data_sorted = DATA.sort_values(by='Зарплата')
                tki.messagebox.showinfo(
                    "Информация", "Отсортированный файл сохранён\
                        в Output/Data_sorted_in_ascending_order.csv")
                way = (DIRECTORY_WAY +
                       "/Output/Data_sorted_in_ascending_order.csv")
                data_sorted.to_csv(f"{way}", sep=",", index=False)
            main_obj = MakeTable(way, length, frame_tabels, 'utf-8')
            main_tree = main_obj.tree
            main_tree.pack(side=tki.BOTTOM, fill=tki.BOTH, expand=tki.YES)
            frame_tabels.pack()  # положение
            win_new.destroy()
            win_table.mainloop()

    button1_ok = tki.Button(win_new,
                            text='Ок',
                            height=1,
                            width=10,
                            command=choose_sort,
                            cursor='hand2')
    button1_ok.place(relx=.4, rely=.2)
    win_new.mainloop()


def make_window_plot(drawn_figure):
    """
    Автор: Максим Колпаков
    -----------------------
    Создание окна для графика
    Параметры
    ----------
    drawn_figure : matplotlib.figure.Figure
          выбранный график
    Возвращает
    -------
    построенный график
    """
    win_new = tki.Toplevel(WIN_MAIN)
    win_new.title("График")
    canvas = FigureCanvasTkAgg(drawn_figure, master=win_new)
    canvas.get_tk_widget().pack()
    canvas.draw()
    btn_exit = tki.Button(win_new,
                          text='Выход',
                          font=('Arial', 15),
                          bg='grey',
                          fg='yellow',
                          height=1,
                          width=10,
                          command=win_new.destroy,
                          cursor='hand2')
    btn_exit.pack(side="bottom")
    win_new.mainloop()


def construct(selected):
    """
    Автор: Максим Колпаков
    -----------------------
    Построение графиков №1 №2 №3 из comboChoosePlot
    Параметры
    ----------
    selected : str
                название графика из comboChoosePlot
    Возвращает
    -------
    график в отдельном окне
    """
    if selected == 'Кол-во профессий по специализациям':
        fig = first(DATA)
        make_window_plot(fig)
    elif selected == 'Зависимость средней зарплаты от специализации':
        fig = second(DATA)
        make_window_plot(fig)
    elif selected == 'Распределение количества вакансий от зп. в городе':
        win_selection = tki.Tk()
        win_selection.title("Выбор города")
        win_selection.geometry("300x100")
        combo_example = ttk.Combobox(win_selection,
                                     state="readonly",
                                     width=50,
                                     values=list(np.unique(DATA['Город'])))
        combo_example.current(0)
        combo_example.pack(padx=10, pady=10)

        def third_plot_call():
            """
            Автор: Татьяна Рыкова
            -----------------------
            Построение графиков №4 №5 из comboChoosePlot
            Возвращает
            -------
            график в отдельном окне
            """
            selected = combo_example.get()
            win_selection.destroy()
            third(selected)

        btn_ok = tki.Button(win_selection, text='Ок',
                            width=10, command=third_plot_call)
        btn_ok.pack(padx=10, pady=10)
        win_selection.mainloop()
    elif (selected ==
          'Кол-во вакансий по специализациям в зависимости от города'):
        fig = fourth(DATA)
        make_window_plot(fig)
    elif (selected ==
          'Кол-во очных и дистанционных вакансий по специализациям'):
        fig = fifth(DATA)
        make_window_plot(fig)


class Window(tki.Tk):
    """
    Автор: Владислав Огай
    -----------------------
    Класс для создания окна Tk()
    """

    def __init__(self):
        """
        Устанавливает все необходимые атрибуты для объекта Window
        """
        super().__init__()
        self.frame_tabels = ttk.LabelFrame(
            self, text='Загруженная база данных')
        self.title("Python project")
        length = 0
        self.main_obj = MakeTable(BASE_WAY, length, self.frame_tabels, 'utf-8')
        self.main_tree = self.main_obj.tree
        self.main_tree.pack(side=tki.BOTTOM, fill=tki.BOTH, expand=tki.YES)
        self.frame_tabels.pack()


choose_the_way()
if len(WAYS) == 3:
    global DIRECTORY_WAY
    global GRAPH_WAY
    global BASE_WAY
    DIRECTORY_WAY = WAYS[0]
    GRAPH_WAY = WAYS[1]
    BASE_WAY = WAYS[2]
    initialize_main_window()
