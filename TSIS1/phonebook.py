import json
from datetime import datetime
from connect import get_connection


def search_contacts():
    query = input("Введите для поиска (имя, телефон или email): ").strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        print("Ничего не найдено.")
    else:
        print(f"\n{'ID':<5} {'Имя':<20} {'Email':<25} {'Группа':<10} {'Телефон':<15} {'Тип'}")
        print("-" * 85)
        for row in rows:
            print(f"{row[0]:<5} {str(row[1]):<20} {str(row[2] or ''):<25} {str(row[4] or ''):<10} {str(row[5] or ''):<15} {str(row[6] or '')}")


def filter_by_group():
    print("\nГруппы: Family, Work, Friend, Other")
    group = input("Введите группу: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
        ORDER BY c.name
    """, (group,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        print("Контакты не найдены.")
    else:
        print(f"\n{'ID':<5} {'Имя':<20} {'Email':<25} {'День рождения':<15} {'Группа'}")
        print("-" * 75)
        for row in rows:
            print(f"{row[0]:<5} {str(row[1]):<20} {str(row[2] or ''):<25} {str(row[3] or ''):<15} {str(row[4] or '')}")


def show_sorted():
    print("\nСортировка:")
    print("  1. По имени")
    print("  2. По дню рождения")
    print("  3. По дате добавления")
    choice = input("Выбор: ").strip()

    order = "c.name"
    if choice == "2":
        order = "c.birthday"
    elif choice == "3":
        order = "c.id"

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY {order}
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    print(f"\n{'ID':<5} {'Имя':<20} {'Email':<25} {'День рождения':<15} {'Группа'}")
    print("-" * 75)
    for row in rows:
        print(f"{row[0]:<5} {str(row[1]):<20} {str(row[2] or ''):<25} {str(row[3] or ''):<15} {str(row[4] or '')}")


def show_paged():
    page = int(input("Номер страницы: ").strip())
    size = int(input("Контактов на странице: ").strip())
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paged(%s, %s)", (page, size))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        print("Нет контактов на этой странице.")
    else:
        print(f"\n{'ID':<5} {'Имя':<20} {'Телефон'}")
        print("-" * 40)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]}")


def add_contact():
    name = input("Имя: ").strip()
    email = input("Email (Enter чтобы пропустить): ").strip() or None
    birthday = input("День рождения (YYYY-MM-DD, Enter чтобы пропустить): ").strip() or None

    print("\nГруппы: Family, Work, Friend, Other")
    group_name = input("Группа (Enter чтобы пропустить): ").strip() or None

    conn = get_connection()
    cur = conn.cursor()

    group_id = None
    if group_name:
        cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
        result = cur.fetchone()
        if result:
            group_id = result[0]

    cur.execute(
        "INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s) RETURNING id",
        (name, email, birthday, group_id)
    )
    contact_id = cur.fetchone()[0]

    phone = input("Телефон (Enter чтобы пропустить): ").strip()
    if phone:
        print("Тип: home / work / mobile")
        phone_type = input("Тип телефона: ").strip()
        cur.execute(
            "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
            (contact_id, phone, phone_type)
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Контакт добавлен!")


def add_phone():
    name = input("Имя контакта: ").strip()
    phone = input("Телефон: ").strip()
    print("Тип: home / work / mobile")
    phone_type = input("Тип: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
    conn.commit()
    cur.close()
    conn.close()
    print("Телефон добавлен!")


def move_to_group():
    name = input("Имя контакта: ").strip()
    group = input("Группа (Family/Work/Friend/Other или новая): ").strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL move_to_group(%s, %s)", (name, group))
    conn.commit()
    cur.close()
    conn.close()
    print("Готово!")


def export_json():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday::text, g.name,
               array_agg(p.phone) as phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    contacts = []
    for row in rows:
        contacts.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "birthday": row[3],
            "group": row[4],
            "phones": [p for p in row[5] if p]
        })

    filename = f"contacts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)
    print(f"Экспортировано в {filename}")


def import_json():
    filename = input("Введите путь к JSON файлу: ").strip()
    with open(filename, encoding="utf-8") as f:
        contacts = json.load(f)

    conn = get_connection()
    cur = conn.cursor()

    for contact in contacts:
        cur.execute("SELECT id FROM contacts WHERE name = %s", (contact["name"],))
        exists = cur.fetchone()

        if exists:
            answer = input(f"Контакт '{contact['name']}' уже есть. Перезаписать? (y/n): ").strip()
            if answer.lower() != "y":
                continue
            cur.execute(
                "UPDATE contacts SET email=%s, birthday=%s WHERE name=%s",
                (contact.get("email"), contact.get("birthday"), contact["name"])
            )
        else:
            cur.execute(
                "INSERT INTO contacts (name, email, birthday) VALUES (%s, %s, %s)",
                (contact["name"], contact.get("email"), contact.get("birthday"))
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Импорт завершён!")


def main():
    while True:
        print("\n=== PhoneBook TSIS1 ===")
        print("1. Поиск контакта")
        print("2. Фильтр по группе")
        print("3. Показать с сортировкой")
        print("4. Показать постранично")
        print("5. Добавить контакт")
        print("6. Добавить телефон к контакту")
        print("7. Переместить в группу")
        print("8. Экспорт в JSON")
        print("9. Импорт из JSON")
        print("10. Выход")

        choice = input("Выбор: ").strip()

        if choice == "1":
            search_contacts()
        elif choice == "2":
            filter_by_group()
        elif choice == "3":
            show_sorted()
        elif choice == "4":
            show_paged()
        elif choice == "5":
            add_contact()
        elif choice == "6":
            add_phone()
        elif choice == "7":
            move_to_group()
        elif choice == "8":
            export_json()
        elif choice == "9":
            import_json()
        elif choice == "10":
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()
