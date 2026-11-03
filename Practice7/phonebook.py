import csv
from connect import connect, create_table


def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
                    (name, phone)
                )
        print("Contact added!")
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()


def import_csv():
    filename = input("Enter CSV filename: ")

    conn = connect()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            with conn:
                with conn.cursor() as cur:
                    for row in reader:
                        cur.execute(
                            """
                            INSERT INTO phonebook (first_name, phone)
                            VALUES (%s, %s)
                            ON CONFLICT (phone) DO NOTHING
                            """,
                            (row["first_name"], row["phone"])
                        )

        print("CSV imported!")
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()


def show_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook ORDER BY id")
    contacts = cur.fetchall()

    for contact in contacts:
        print(contact)

    cur.close()
    conn.close()


def search_contact():
    print("1. Search by name")
    print("2. Search by phone")
    print("3. Search by phone prefix")

    choice = input("Choose: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE first_name ILIKE %s",
            ("%" + name + "%",)
        )

    elif choice == "2":
        phone = input("Enter phone: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE phone = %s",
            (phone,)
        )

    elif choice == "3":
        prefix = input("Enter prefix: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE phone LIKE %s",
            (prefix + "%",)
        )

    else:
        print("Invalid choice!")
        cur.close()
        conn.close()
        return

    contacts = cur.fetchall()

    for contact in contacts:
        print(contact)

    cur.close()
    conn.close()


def update_contact():
    phone = input("Enter current phone: ")

    print("1. Update name")
    print("2. Update phone")

    choice = input("Choose: ")

    conn = connect()

    try:
        with conn:
            with conn.cursor() as cur:
                if choice == "1":
                    name = input("Enter new name: ")
                    cur.execute(
                        "UPDATE phonebook SET first_name = %s WHERE phone = %s",
                        (name, phone)
                    )

                elif choice == "2":
                    new_phone = input("Enter new phone: ")
                    cur.execute(
                        "UPDATE phonebook SET phone = %s WHERE phone = %s",
                        (new_phone, phone)
                    )

                else:
                    print("Invalid choice!")
                    return

                if cur.rowcount == 0:
                    print("Contact not found!")
                else:
                    print("Contact updated!")

    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()


def delete_contact():
    print("1. Delete by name")
    print("2. Delete by phone")

    choice = input("Choose: ")

    conn = connect()

    try:
        with conn:
            with conn.cursor() as cur:
                if choice == "1":
                    name = input("Enter name: ")
                    cur.execute(
                        "DELETE FROM phonebook WHERE first_name = %s",
                        (name,)
                    )

                elif choice == "2":
                    phone = input("Enter phone: ")
                    cur.execute(
                        "DELETE FROM phonebook WHERE phone = %s",
                        (phone,)
                    )

                else:
                    print("Invalid choice!")
                    return

                if cur.rowcount == 0:
                    print("Contact not found!")
                else:
                    print("Contact deleted!")

    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()


def main():
    create_table()

    while True:
        print("\n--- PHONEBOOK ---")
        print("1. Add contact")
        print("2. Import from CSV")
        print("3. Show all contacts")
        print("4. Search contact")
        print("5. Update contact")
        print("6. Delete contact")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            import_csv()
        elif choice == "3":
            show_contacts()
        elif choice == "4":
            search_contact()
        elif choice == "5":
            update_contact()
        elif choice == "6":
            delete_contact()
        elif choice == "0":
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
