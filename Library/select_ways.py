import tkinter as tki
from tkinter import filedialog
WAYS = []


def choose_the_way():
    """
    Автор: Татьяна Рыкова
    -----------------------
    Окно для выбора папки проекта и файла с базой данных
    Возвращает
    -------
    None
    """
    choose_way = tki.Tk()
    choose_way.title("Начало работы")

    def output_dir():
        """
        Автор: Максим Колпаков
        -----------------------
        Отображение названия директории,
        выбранной пользователем в поле EntryDir окна choose_way
        Возвращает
        -------
        None
        """
        global DIRECTORY_WAY
        directory = filedialog.askdirectory(
            initialdir="/", title="Select directory")
        DIRECTORY_WAY = directory
        entry_dir.config(state="normal")
        entry_dir.delete(0, 'end')
        entry_dir.insert(tki.END, DIRECTORY_WAY)
        entry_dir.config(state="readonly")

    def output_base():
        """
        Автор: Максим Колпаков
        -----------------------
        Отображение названия файла с базой данных, выбранного пользователем,
        в поле EntryBase окна choose_way
        Возвращает
        -------
        None
        """
        global BASE_WAY
        filename = filedialog.askopenfilename(
            initialdir="/",
            title="Select file",
            filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        BASE_WAY = filename
        entry_base.config(state="normal")
        entry_base.delete(0, 'end')
        entry_base.insert(tki.END, BASE_WAY)
        entry_base.config(state="readonly")

    def output_graph():
        """
        Автор: Максим Колпаков
        -----------------------
        Отображение названия директории,
        выбранной пользователем в поле EntryGraph окна choose_way
        Возвращает
        -------
        None
        """
        global GRAPH_WAY
        graph = filedialog.askdirectory(
            initialdir="/", title="Select directory")
        GRAPH_WAY = graph
        entry_graph.config(state="normal")
        entry_graph.delete(0, 'end')
        entry_graph.insert(tki.END, GRAPH_WAY)
        entry_graph.config(state="readonly")

    frame_for_directories = tki.Frame(choose_way)
    frame_for_directories.pack()
    label_dir = tki.Label(
        frame_for_directories,
        text="Выберите рабочую директорию для сохранения файлов",
        font="Arial 11",
        fg="black")
    label_dir.pack()
    entry_dir = tki.Entry(frame_for_directories, width=40, state='readonly')
    entry_dir.pack()
    button_dir = tki.Button(frame_for_directories,
                            text="Выбрать",
                            command=output_dir)
    button_dir.pack()
    label_graph = tki.Label(
        frame_for_directories,
        text="Выберите рабочую директорию для сохранения графиков",
        font="Arial 11",
        fg="black")
    label_graph.pack()
    entry_graph = tki.Entry(frame_for_directories, width=40, state='readonly')
    entry_graph.pack()
    button_graph = tki.Button(
        frame_for_directories,
        text="Выбрать",
        command=output_graph)
    button_graph.pack()
    label_base = tki.Label(
        frame_for_directories,
        text="Выберите нужную базу данных",
        font="Arial 11",
        fg="black")
    label_base.pack()
    entry_base = tki.Entry(frame_for_directories, width=40, state='readonly')
    entry_base.pack()
    button_base = tki.Button(frame_for_directories,
                             text="Выбрать",
                             command=output_base)
    button_base.pack()

    def check_ways():
        """
        Автор: Татьяна Рыкова
        -----------------------
        Проверка полей entry_dir и entryBase на наличие данных,
        переход к главному окну приложения
        Возвращает
        -------
        None
        """
        if (entry_dir.get() == ""
            or entry_base.get() == ""
                or entry_graph.get() == ""):
            tki.messagebox.showinfo(
                "Ошибка", "Проверьте правильность введённых данных")
        else:
            WAYS.append(DIRECTORY_WAY)
            WAYS.append(GRAPH_WAY)
            WAYS.append(BASE_WAY)
            choose_way.destroy()

    button2_ok = tki.Button(
        frame_for_directories,
        text="Ок",
        command=check_ways)
    button2_ok.pack()
    choose_way.mainloop()
