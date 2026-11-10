import json
from connect import connect


def print_contacts(rows):
    if not rows:
        print("No contacts found.")
        return

    for contact_id, first_name, last_name, phone in rows:
        print(f"{contact_id}: {first_name} {last_name} - {phone}")


def search_contacts():
    pattern = input("Enter part of name, surname or phone: ").strip()

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM search_contacts(%s)",
                (pattern,)
            )
            print_contacts(cur.fetchall())


def upsert_contact():
    first_name = input("First name: ").strip()
    last_name = input("Last name (optional): ").strip()
    phone = input("Phone: ").strip()

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL upsert_contact(%s, %s, %s)",
                (first_name, last_name, phone)
            )

    print("Contact added or updated!")


def bulk_insert_contacts():
    count = int(input("How many contacts? "))

    if count < 1:
        print("Enter a positive number.")
        return

    contacts = []

    for i in range(count):
        print(f"Contact {i + 1}:")

        contacts.append({
            "first_name": input("First name: ").strip(),
            "last_name": input("Last name (optional): ").strip(),
            "phone": input("Phone: ").strip()
        })

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL bulk_insert_contacts(%s::jsonb, NULL)",
                (json.dumps(contacts),)
            )

            invalid = cur.fetchone()[0]

    print(f"Processed {count} contacts. Invalid: {len(invalid)}")

    for item in invalid:
        print(item)


def show_page():
    limit = int(input("Contacts per page: "))
    page = int(input("Page number (starting from 1): "))

    if limit < 1 or page < 1:
        print("Limit and page must be positive.")
        return

    offset = (page - 1) * limit

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_contacts_page(%s, %s)",
                (limit, offset)
            )

            print_contacts(cur.fetchall())


def delete_contact():
    choice = input("Delete by 1 = name, 2 = phone: ").strip()

    if choice == "1":
        name = input("First name: ").strip()
        params = (name, None)

    elif choice == "2":
        phone = input("Phone: ").strip()
        params = (None, phone)

    else:
        print("Invalid choice.")
        return

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL delete_contact(%s, %s)",
                params
            )

    print("Delete procedure completed!")


def main():
    while True:
        print("\n PHONEBOOK")
        print("1. Search contacts")
        print("2. Add or update contact")
        print("3. Add multiple contacts")
        print("4. Show contacts by page")
        print("5. Delete contact")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            search_contacts()

        elif choice == "2":
            upsert_contact()

        elif choice == "3":
            bulk_insert_contacts()

        elif choice == "4":
            show_page()

        elif choice == "5":
            delete_contact()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
