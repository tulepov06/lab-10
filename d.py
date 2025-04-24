import psycopg2
import csv
from tabulate import tabulate

# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    dbname="phones",
    user="postgres",
    password="123456789",
    port=5432
)

cur = conn.cursor()


# Инфо енгізу функциясы
def insert_data():
    print('Type "csv" or "con" to choose option between uploading csv file or typing from console: ')
    method = input().lower() #(csv немесе con)
    
    if method == "con":
        name = input("Name: ")
        surname = input("Surname: ")
        phone = input("Phone: ")
        cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (name, surname, phone))
        conn.commit() # Мәліметтер қорына сақтау(Тэблге сактау)
        print(" Данные успешно добавлены.")
        display_data()# Тэблды корсетеды


    elif method == "csv": # CSV файлы арқылы енгізу
        filepath = ('/Users/alizhantulep/Desktop/Pygame/pygame/data.csv')
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            next(reader) # Бірінші жолды өткізіп жіберу
            for row in reader:
                cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", tuple(row))
        conn.commit() 
        print("✅ Данные успешно добавлены.")
        display_data()  
 

def update_data():
    column = input('Что хотите обновить (name/surname/phone): ').lower()  # Қай бағанды жаңартқысы келетінін сұрау
    value = input(f"Введите текущее значение {column}: ") # Ескі мән
    new_value = input(f"Введите новое значение {column}: ") # Жаңа мән
    cur.execute(f"UPDATE phonebook SET {column} = %s WHERE {column} = %s", (new_value, value))
    conn.commit()

# Телефон нөмірі бойынша өшіру
def delete_data():
    phone = input('Введите номер телефона для удаления: ')
    cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    conn.commit()

#pattern
def query_data():
    column = input("Введите имя столбца (name/surname/phone): ")
    value = input(f"Введите значение для поиска: ")
    cur.execute(f"SELECT * FROM phonebook WHERE {column} = %s", (value,))
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt="fancy_grid"))

def display_data():
    cur.execute("SELECT * FROM phonebook;")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt='fancy_grid'))


#pattern
def search_by_pattern():
    name = input("Введите часть имени: ")
    surname = input("Введите часть фамилии: ")
    phone = input("Введите часть номера телефона: ")
    cur.execute("SELECT * FROM search_by_pattern(%s, %s, %s)", (name, surname, phone))
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt="fancy_grid"))

# Қолданушыны қосу немесе жаңарту (бар болса жаңартылады)
def add_or_update_user():
    name = input("Имя: ")
    surname = input("Фамилия: ")
    phone = input("Телефон: ")
    cur.execute("CALL add_or_update_user(%s, %s, %s)", (name, surname, phone))
    conn.commit()
    print("Пользователь добавлен или обновлён.")

# Көп қолданушыны бірден қосу
def bulk_insert():
    count = int(input("Сколько пользователей хотите добавить? "))
    names, surnames, phones = [], [], []

    for i in range(count):
        print(f"\nПользователь {i+1}:")
        names.append(input("Имя: "))
        surnames.append(input("Фамилия: "))
        phones.append(input("Телефон: "))

    cur.execute("CALL bulk_insert_users(%s, %s, %s)", (names, surnames, phones))
    conn.commit()

# Пагинация
def get_paginated():
    limit = int(input("Сколько записей показать (LIMIT): "))
    offset = int(input("Со смещения (OFFSET): "))
    cur.execute("SELECT * FROM get_users_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt="fancy_grid"))

# Аты, тегі немесе номері бойынша өшіру
def delete_by_info():
    name = input("Имя (можно оставить пустым): ") or None
    surname = input("Фамилия (можно оставить пустым): ") or None
    phone = input("Телефон (можно оставить пустым): ") or None
    cur.execute("CALL delete_by_name_or_phone(%s, %s, %s)", (name, surname, phone))
    conn.commit()
    print("Удаление завершено.")

# команданын меню
while True:
    print("""
    ===== МЕНЮ ТЕЛЕФОННОЙ КНИГИ =====
    1. "1"     - Вставить данные (CSV/ручной ввод)
    2. "2"     - Обновить данные
    3. "3"     - Поиск по точному совпадению
    4. "4"     - Удалить по номеру телефона
    5. "5"     - Показать всю таблицу
    6. "6"     - Выйти из программы
    ----------------------------
    7. "7"  - Поиск по шаблону
    8. "8"  - Добавить/обновить 
    9. "9"     - Массовое добавление
    10. "10"    - Пагинация (LIMIT/OFFSET)
    11. "11" - Удаление по имени/фамилии/номеру
    """)

    command = input("Введите команду: ").lower()

    if command == "1":
        insert_data()
    elif command == "2":
        update_data()
    elif command == "3":
        query_data()
    elif command == "4":
        delete_data()
    elif command == "5":
        display_data()
    elif command == "7":
        search_by_pattern()
    elif command == "8":
        add_or_update_user()
    elif command == "9":
        bulk_insert()
    elif command == "10":
        get_paginated()
    elif command == "11":
        delete_by_info()
    elif command == "6":
        break
    else:
        print("Неизвестная команда. Попробуйте снова.")

conn.commit()
cur.close()
conn.close()