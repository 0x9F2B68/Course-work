"""
Есть записи о деталях выпускаемых цехом предприятия.
Написать программу для формирования справки деталей массой более 1 кг
"""

from tkinter import *
from tkinter import ttk
from dbandgist import *

root = Tk()
root.title("Курсовая работа")
w_center = root.winfo_screenwidth()
h_center = root.winfo_screenheight()
form_geometry = '800x380+500+200'  # размер и положение окна
root.configure(bg='#5DCFC3')
root.geometry(form_geometry)
root.resizable(False, False)

# label 1
Label(text='Детали:', font=('Comic Sans MS', 12), background='#5DCFC3', foreground='#000000').grid(row=0, column=5)

# label 2
Label(text='Фильтр по массе:', font=('Comic Sans MS', 12), background='#5DCFC3', foreground='#000000').grid(row=3,
                                                                                                            column=2)

# label 3
Label(text='Справка:', font=('Comic Sans MS', 12), background='#5DCFC3', foreground='#000000').grid(row=0, column=2)

# filter entry
filter_entry = Entry(width=25)
filter_entry.insert(0, "Все")
filter_entry.grid(row=3, column=3)

# table of details
tree = ttk.Treeview()
tree.grid(row=1, column=5)
tree["columns"] = ("Название детали", "Тип", "Масса", "Материал")
tree.column("#0", width=35, minwidth=25)
tree.column("Название детали", width=150, minwidth=150)
tree.column("Тип", width=100, minwidth=100)
tree.column("Масса", width=60, minwidth=60)
tree.column("Материал", width=100, minwidth=50)

tree.heading("#0", text="ID")
tree.heading("Название детали", text="Название детали")
tree.heading("Тип", text="Тип")
tree.heading("Масса", text="Масса")
tree.heading("Материал", text="Материал")

# add button
''' form of adding detail '''
det_id = StringVar()
det_name = StringVar()
det_type = StringVar()
det_mass = StringVar()
det_mat = StringVar()


def add_item(event):
    window = Toplevel(root)
    window.title("Добавить деталь")
    Label(window, text="id детали").grid(row=0, column=0)
    Entry(window, width=50, textvariable=det_id).grid(row=0, column=1)
    Label(window, text="Название детали").grid(row=1, column=0)
    Entry(window, width=50, textvariable=det_name).grid(row=1, column=1)
    Label(window, text="Тип детали").grid(row=2, column=0)
    Entry(window, width=50, textvariable=det_type).grid(row=2, column=1)
    Label(window, text="Масса детали (в г.)").grid(row=3, column=0)
    Entry(window, width=50, textvariable=det_mass).grid(row=3, column=1)
    Label(window, text="Материал детали").grid(row=4, column=0)
    Entry(window, width=50, textvariable=det_mat).grid(row=4, column=1)
    adding_to_BD_button = Button(window, text='Добавить', font=('', 12),
                                 activebackground='#8D9299',
                                 height=1, width=10, bd=0)

    # button action - adding to BD
    def adding_to_BD(event):
        if det_id.get() or det_name.get() or det_type.get() or det_mass.get() or det_mat.get() != '':
            add_detail(int(det_id.get()), det_name.get(), det_type.get(), int(det_mass.get()), det_mat.get())
            window.destroy()

    adding_to_BD_button.bind('<ButtonRelease-1>', adding_to_BD)
    adding_to_BD_button.grid(row=10, column=0)
    closing_button = Button(window, text='Закрыть', font=('', 12),
                            activebackground='#8D9299',
                            height=1, width=10, bd=0)
    closing_button.config(command=window.destroy)
    closing_button.grid(row=10, column=1)


''' button landing '''
add_button = Button(text='Добавить', font=('Comic Sans MS', 12),
                    fg='#000000', bg='#00675C', activebackground='#8D9299', activeforeground='#23272A',
                    height=1, width=15, bd=0)

add_button.bind('<ButtonRelease-1>', add_item)
add_button.grid(row=2, column=2)

# delete button
''' form of deleting detail '''


def delete_item(event):
    window = Toplevel(root)
    window.title("Удалить деталь")
    window.geometry('300x78+400+170')
    Label(window, text="Введи id детали:", font=('Comic Sans MS', 12)).grid(row=0, column=0)
    Entry(window, width=60, textvariable=det_id).grid(row=0, column=1)

    closing_button = Button(window, text='Удалить и закрыть', font=('', 12),
                            activebackground='#8D9299', background='#999999',
                            height=1, width=15, bd=0)

    # button action - deleting from BD
    def deleting(event):
        if det_id.get() != '':
            remove_detail(int(det_id.get()))
        window.destroy()

    Label(window, text=' ').grid(row=1, column=0)
    closing_button.bind('<ButtonRelease-1>', deleting)
    closing_button.grid(row=2, column=0)


''' button landing '''
delete_button = Button(text='Удалить', font=('Comic Sans MS', 12),
                       fg='#000000', bg='#00675C', activebackground='#8D9299', activeforeground='#23272A',
                       height=1, width=15, bd=0)
delete_button.bind('<ButtonRelease-1>', delete_item)
delete_button.grid(row=2, column=3)

# label of count details
text_in_count_label = ''
count_label = Label(text=text_in_count_label, font=('Comic Sans MS', 12), background='#5DCFC3', foreground='#000000')
count_label.grid(row=1, column=2)

# label of mass of all details
text_in_mass_label = ''
mass_label = Label(text=text_in_mass_label, font=('Comic Sans MS', 12), background='#5DCFC3', foreground='#000000')
mass_label.grid(row=1, column=3)


# reference button
def refresh(event):
    count = 0
    summ_mass = 0
    tree.delete(*tree.get_children())  # очистка таблицы
    if filter_entry.get() == 'Все' or filter_entry.get() == 'все' or filter_entry.get() == '':
        data = select_all()
    else:
        data = find_details_by_mass(filter_entry.get())
    for i in data:
        tree.insert("", "end", iid=None, text=i[0], values=(i[1], i[2], i[3], i[4]))
        count += 1
        summ_mass += i[3]
    text_in_count_label = 'Кол-во деталей:\n' + str(count)
    text_in_mass_label = 'Масса деталей:\n' + str(summ_mass)
    count_label.config(text=text_in_count_label)
    mass_label.config(text=text_in_mass_label)


''' button landing '''
reference_button = Button(text='Сформировать справку', font=('Impact', 13),
                          fg='#000000', bg='#FFA500', activebackground='#8D9299', activeforeground='#23272A',
                          height=1, width=55, bd=0)
reference_button.bind('<ButtonRelease-1>', refresh)
reference_button.grid(row=2, column=5)


# diagram button
def draw_diagram(event):
    data = select_all()
    values = []
    labels = []
    temp = 0
    for i in data:
        if i[2] in labels:
            pass
        else:
            detail_types = find_details_by_type(i[2])
            labels.append(i[2])
            values.append(0)
            for j in detail_types:
                values[temp] += j[3]
            temp += 1
    print(values, labels)
    draw_pie_chart(tuple(labels), tuple(values))


""" button landing """
diagram_button = Button(text='Диаграмма', font=('Impact', 13),
                        fg='#000000', bg='#FFA500', activebackground='#8D9299', activeforeground='#23272A',
                        height=1, width=55, bd=0)
diagram_button.grid(row=3, column=5)
diagram_button.bind('<ButtonRelease-1>', draw_diagram)

# about button
''' form about '''


def about(event):
    window = Toplevel(root)
    window.title("Об авторе")
    # window.geometry('400x150')
    window.overrideredirect()
    Label(window, text="Программу разработал:\n"
                       "Richard Tesla (VTM) \n"
                       "tg: @embwave\n"
                       "github.com/0x9F2B68", font=('Comic Sans MS', 13)).grid(row=0)
    Label(window, text=' ').grid(row=1)
    closing_button = Button(window, text='Закрыть', font=('', 11),
                            activebackground='#8D9299', background='#999999',
                            height=1, width=15, bd=0)
    closing_button.grid(row=3)
    closing_button.config(command=window.destroy)


''' button landing '''
about_button = Button(text='О себе', font=('Comic Sans MS', 12),
                      fg='#000000', bg='#00675C', activebackground='#8D9299', activeforeground='#23272A',
                      height=1, width=15, bd=0)
about_button.bind('<ButtonRelease-1>', about)
about_button.grid(row=4, column=3)


# exit button
def app_quit(event):
    root.destroy()


''' button landing '''
exit_button = Button(text='Выход', font=('Comic Sans MS', 12),
                     fg='#FFFFFF', bg='#FF4040', activebackground='#8D9299', activeforeground='#23272A',
                     height=1, width=15, bd=0)
exit_button.bind('<ButtonRelease-1>', app_quit)
exit_button.grid(row=4, column=2)
root.mainloop()
