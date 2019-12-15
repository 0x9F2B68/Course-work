import sqlite3
import matplotlib.pyplot as plt


def create_table_details():
    """Создание таблицы деталей"""
    conn = sqlite3.connect('Workshop.db')
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS Details (detail_id INT PRIMARY KEY, detail_name TEXT, detail_type TEXT, mass INT, material INT)")
    conn.commit()
    c.close()
    conn.close()


def add_detail(detail_id, detail_name, detail_type, mass, material):
    """Добавление детали"""
    conn = sqlite3.connect('Workshop.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO Details VALUES (?,?,?,?,?)",
              (detail_id, detail_name, detail_type, mass, material))
    conn.commit()
    c.close()
    conn.close()


def remove_detail(detail_id):
    """Удаление детали"""
    conn = sqlite3.connect('Workshop.db')
    c = conn.cursor()
    c.execute("DELETE FROM Details WHERE detail_id = (?)", (detail_id,))
    conn.commit()
    c.close()
    conn.close()


def find_details_by_mass(mass):
    """Поиск детали по массе"""
    conn = sqlite3.connect('Workshop.db')
    c = conn.cursor()
    c.execute('SELECT * FROM Details WHERE mass >= (?)', (mass,))
    data = c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return data


def find_details_by_type(detail_type):
    """Поиск детали по типу"""
    conn = sqlite3.connect('Workshop.db')
    c = conn.cursor()
    c.execute('SELECT * FROM Details WHERE detail_type = (?)', (detail_type,))
    data = c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return data


def select_all():
    """Вывод всех деталей"""
    conn = sqlite3.connect('Workshop.db')
    c = conn.cursor()
    c.execute('SELECT * FROM Details ORDER BY detail_id')
    data = c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return data


def draw_pie_chart(labels, values):
    try:
        sizes = []
        for v in values:
            sizes.append(v / sum(values) * 100)
        plt.subplots()
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()
    except Exception as e:
        print('Не удалось построить круговую диаграмму\n', e)

def main():
    create_table_details()
    add_detail(1, '1-КЛ-230', 'Болт', 720, 'Сталь')
    add_detail(2, '1-КЛ-231', 'Болт', 600, 'Сталь')
    print(select_all())
    remove_detail(2)
    print(find_details_by_mass(700))


if __name__ == '__main__':
    main()
