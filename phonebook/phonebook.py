import csv
from connect import get_connection


def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id    SERIAL PRIMARY KEY,
            name  VARCHAR(100) NOT NULL,
            phone VARCHAR(20)  NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def add_contact():
    name = input("Введите имя: ").strip()
    phone = input("Введите телефон: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Контакт добавлен!")


def import_csv():
    filename = input("Введите путь к CSV файлу: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        with open(filename, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            count = 0
            for row in reader:
                if len(row) < 2:
                    continue
                cur.execute(
                    "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                    (row[0].strip(), row[1].strip())
                )
                count += 1
        conn.commit()
        print(f"Импортировано {count} контакт(ов)!")

    except FileNotFoundError:
        print("Файл не найден.")
    except Exception as e:
        conn.rollback()
        print("Ошибка:", e)
    finally:
        cur.close()
        conn.close()


def show_contacts():
    print("\nФильтр:")
    print("  1. Показать всех")
    print("  2. Поиск по имени")
    print("  3. Поиск по префиксу телефона")
    choice = input("Выбор: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    if choice == "2":
        name = input("Введите имя (или часть): ").strip()
        cur.execute(
            "SELECT id, name, phone FROM phonebook WHERE name ILIKE %s ORDER BY name",
            (f"%{name}%",)
        )
    elif choice == "3":
        prefix = input("Введите префикс телефона: ").strip()
        cur.execute(
            "SELECT id, name, phone FROM phonebook WHERE phone LIKE %s ORDER BY name",
            (f"{prefix}%",)
        )
    else:
        cur.execute("SELECT id, name, phone FROM phonebook ORDER BY name")

    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        print("Контакты не найдены.")
    else:
        print(f"\n{'ID':<5} {'Имя':<20} {'Телефон'}")
        print("-" * 40)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]}")


def update_contact():
    print("\nОбновить по:")
    print("  1. Имени")
    print("  2. Телефону")
    choice = input("Выбор: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        old_name = input("Текущее имя: ").strip()
        print("Что обновить?")
        print("  1. Имя")
        print("  2. Телефон")
        field = input("Выбор: ").strip()
        if field == "1":
            new_name = input("Новое имя: ").strip()
            cur.execute(
                "UPDATE phonebook SET name = %s WHERE name = %s",
                (new_name, old_name)
            )
        else:
            new_phone = input("Новый телефон: ").strip()
            cur.execute(
                "UPDATE phonebook SET phone = %s WHERE name = %s",
                (new_phone, old_name)
            )
    elif choice == "2":
        old_phone = input("Текущий телефон: ").strip()
        print("Что обновить?")
        print("  1. Имя")
        print("  2. Телефон")
        field = input("Выбор: ").strip()
        if field == "1":
            new_name = input("Новое имя: ").strip()
            cur.execute(
                "UPDATE phonebook SET name = %s WHERE phone = %s",
                (new_name, old_phone)
            )
        else:
            new_phone = input("Новый телефон: ").strip()
            cur.execute(
                "UPDATE phonebook SET phone = %s WHERE phone = %s",
                (new_phone, old_phone)
            )
    else:
        print("Неверный выбор.")
        cur.close()
        conn.close()
        return

    conn.commit()
    if cur.rowcount > 0:
        print(f"Обновлено {cur.rowcount} запис(ей).")
    else:
        print("Контакт не найден.")
    cur.close()
    conn.close()


def delete_contact():
    print("\nУдалить по:")
    print("  1. Имени")
    print("  2. Телефону")
    choice = input("Выбор: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        name = input("Введите имя: ").strip()
        cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
    elif choice == "2":
        phone = input("Введите телефон: ").strip()
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    else:
        print("Неверный выбор.")
        cur.close()
        conn.close()
        return

    conn.commit()
    if cur.rowcount > 0:
        print(f"Удалено {cur.rowcount} контакт(ов).")
    else:
        print("Контакт не найден.")
    cur.close()
    conn.close()


def main():
    create_table()

    while True:
        print("\n=== PhoneBook ===")
        print("1. Добавить контакт")
        print("2. Показать / найти контакты")
        print("3. Импорт из CSV")
        print("4. Обновить контакт")
        print("5. Удалить контакт")
        print("6. Выход")

        choice = input("Выбор: ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            show_contacts()
        elif choice == "3":
            import_csv()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            break
        else:
            print("Неверный выбор, попробуй снова.")


if __name__ == "__main__":
    main()
