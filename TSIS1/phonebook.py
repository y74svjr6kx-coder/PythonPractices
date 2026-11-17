import csv
import json
import re
from contextlib import contextmanager
from datetime import date
from pathlib import Path

from connect import connect


PHONE_PATTERN = re.compile(r"\+?[0-9]{10,15}\Z")
PHONE_TYPES = {"home", "work", "mobile"}
SORT_OPTIONS = {
    "1": "pb.first_name ASC, pb.last_name ASC, pb.id ASC",
    "2": "c.birthday ASC NULLS LAST, pb.first_name ASC, pb.id ASC",
    "3": "c.created_at DESC, pb.id DESC",
}


@contextmanager
def database_cursor():
    conn = connect()
    try:
        with conn:
            with conn.cursor() as cur:
                yield cur
    finally:
        conn.close()


def format_contacts(cur, rows):
    contacts = []
    for contact_id, first_name, last_name, email, birthday, group_name, created_at in rows:
        contacts.append({
            "id": contact_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "birthday": birthday.isoformat() if birthday else None,
            "group": group_name or "Other",
            "created_at": created_at.isoformat() if created_at else None,
            "phones": [],
        })

    if contacts:
        ids = [contact["id"] for contact in contacts]
        cur.execute(
            "SELECT contact_id, phone, type FROM phones "
            "WHERE contact_id = ANY(%s) ORDER BY id",
            (ids,),
        )
        by_id = {contact["id"]: contact for contact in contacts}
        for contact_id, phone, phone_type in cur.fetchall():
            by_id[contact_id]["phones"].append({
                "phone": phone,
                "type": phone_type,
            })
    return contacts


def select_contacts(cur, where="TRUE", params=(), order_by=None):
    ordering = order_by or SORT_OPTIONS["1"]
    cur.execute(
        "SELECT pb.id, pb.first_name, pb.last_name, "
        "c.email, c.birthday, g.name, c.created_at "
        "FROM phonebook AS pb "
        "JOIN contacts AS c ON c.id = pb.id "
        "LEFT JOIN groups AS g ON g.id = c.group_id "
        f"WHERE {where} ORDER BY {ordering}",
        params,
    )
    return format_contacts(cur, cur.fetchall())


def display_contacts(contacts):
    if not contacts:
        print("No contacts found.")
        return

    for contact in contacts:
        name = f"{contact['first_name']} {contact['last_name']}".strip()
        phones = ", ".join(
            f"{p['phone']} ({p['type']})" for p in contact["phones"]
        ) or "No phone"
        print(f"\n{contact['id']}: {name}")
        print(f"  Phones: {phones}")
        print(f"  Email: {contact['email'] or '-'}")
        print(f"  Birthday: {contact['birthday'] or '-'}")
        print(f"  Group: {contact['group']}")
        print(f"  Added: {contact['created_at'] or '-'}")


def filter_by_group():
    with database_cursor() as cur:
        cur.execute("SELECT name FROM groups ORDER BY name")
        names = [row[0] for row in cur.fetchall()]
        print("Available groups:", ", ".join(names))
        group = input("Enter group: ").strip()
        contacts = select_contacts(cur, "LOWER(g.name) = LOWER(%s)", (group,))
    display_contacts(contacts)


def search_by_email():
    email_part = input("Enter part of email: ").strip()
    with database_cursor() as cur:
        contacts = select_contacts(cur, "c.email ILIKE %s", (f"%{email_part}%",))
    display_contacts(contacts)


def sort_contacts():
    print("1. Name")
    print("2. Birthday")
    print("3. Date added (newest first)")
    choice = input("Sort by: ").strip()
    if choice not in SORT_OPTIONS:
        print("Invalid sort option.")
        return
    with database_cursor() as cur:
        contacts = select_contacts(cur, order_by=SORT_OPTIONS[choice])
    display_contacts(contacts)


def paginate_contacts():
    per_page = int(input("Contacts per page: "))
    if per_page < 1:
        print("Enter a positive number.")
        return

    page = 1
    while True:
        with database_cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM phonebook")
            total = cur.fetchone()[0]
            max_page = max(1, (total + per_page - 1) // per_page)
            page = min(page, max_page)
            offset = (page - 1) * per_page

            cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (per_page, offset))
            ids = [row[0] for row in cur.fetchall()]

            if ids:
                found = select_contacts(cur, "pb.id = ANY(%s)", (ids,))
                by_id = {item["id"]: item for item in found}
                contacts = [by_id[item_id] for item_id in ids if item_id in by_id]
            else:
                contacts = []

        print(f"\nPage {page}/{max_page} (total: {total})")
        display_contacts(contacts)
        command = input("next / prev / quit: ").strip().lower()
        if command in ("quit", "q"):
            break
        if command in ("next", "n"):
            if page < max_page:
                page += 1
            else:
                print("This is the last page.")
        elif command in ("prev", "p"):
            if page > 1:
                page -= 1
            else:
                print("This is the first page.")
        else:
            print("Enter next, prev or quit.")


def export_json():
    filename = input("Export filename [contacts_export.json]: ").strip()
    destination = Path(filename or "contacts_export.json")
    if destination.exists():
        answer = input("File exists. Overwrite? (yes/no): ").strip().lower()
        if answer != "yes":
            print("Export cancelled.")
            return

    with database_cursor() as cur:
        contacts = select_contacts(cur, order_by="pb.id ASC")
    destination.write_text(
        json.dumps(contacts, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Exported {len(contacts)} contacts to {destination}.")


def validate_contact(raw):
    if not isinstance(raw, dict):
        raise ValueError("Each contact must be a JSON object.")

    first = str(raw.get("first_name") or "").strip()
    last = str(raw.get("last_name") or "").strip()
    email = str(raw.get("email") or "").strip() or None
    birthday = str(raw.get("birthday") or "").strip() or None
    group = str(raw.get("group") or "Other").strip().title()
    phones = raw.get("phones")

    if not first or len(first) > 100 or len(last) > 100:
        raise ValueError("First/last name is empty or too long.")
    if email and (len(email) > 100 or "@" not in email):
        raise ValueError("Invalid email.")
    if birthday:
        birthday = date.fromisoformat(birthday).isoformat()
    if not group or len(group) > 50:
        raise ValueError("Invalid group name.")
    if not isinstance(phones, list) or not phones:
        raise ValueError("At least one phone is required.")

    clean_phones = []
    seen = set()
    for item in phones:
        if not isinstance(item, dict):
            raise ValueError("Each phone must have phone and type fields.")
        phone = str(item.get("phone") or "").strip()
        phone_type = str(item.get("type") or "mobile").strip().lower()
        if not PHONE_PATTERN.fullmatch(phone):
            raise ValueError(f"Invalid phone: {phone}")
        if phone_type not in PHONE_TYPES:
            raise ValueError(f"Invalid phone type: {phone_type}")
        if phone in seen:
            raise ValueError(f"Repeated phone in one contact: {phone}")
        seen.add(phone)
        clean_phones.append({"phone": phone, "type": phone_type})

    return {
        "first_name": first,
        "last_name": last,
        "email": email,
        "birthday": birthday,
        "group": group,
        "phones": clean_phones,
    }


def get_group_id(cur, group_name):
    cur.execute(
        "INSERT INTO groups (name) VALUES (%s) "
        "ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name "
        "RETURNING id",
        (group_name,),
    )
    return cur.fetchone()[0]


def find_contact_ids(cur, first_name, last_name):
    cur.execute(
        "SELECT id FROM phonebook "
        "WHERE LOWER(BTRIM(first_name)) = LOWER(%s) "
        "AND LOWER(BTRIM(last_name)) = LOWER(%s) ORDER BY id",
        (first_name, last_name),
    )
    return [row[0] for row in cur.fetchall()]


def insert_phones(cur, contact_id, phones):
    for item in phones:
        cur.execute(
            "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
            (contact_id, item["phone"], item["type"]),
        )


def save_json_contact(cur, contact, existing_id=None):
    group_id = get_group_id(cur, contact["group"])
    primary_phone = contact["phones"][0]["phone"]

    if existing_id is None:
        cur.execute(
            "INSERT INTO phonebook (first_name, last_name, phone) "
            "VALUES (%s, %s, %s) RETURNING id",
            (contact["first_name"], contact["last_name"], primary_phone),
        )
        contact_id = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO contacts (id, email, birthday, group_id) "
            "VALUES (%s, %s, %s, %s)",
            (contact_id, contact["email"], contact["birthday"], group_id),
        )
    else:
        contact_id = existing_id
        cur.execute(
            "UPDATE phonebook SET phone = %s WHERE id = %s",
            (primary_phone, contact_id),
        )
        cur.execute(
            "UPDATE contacts SET email = %s, birthday = %s, group_id = %s "
            "WHERE id = %s",
            (contact["email"], contact["birthday"], group_id, contact_id),
        )
        cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))

    insert_phones(cur, contact_id, contact["phones"])


def import_json():
    filename = input("JSON filename [contacts_export.json]: ").strip()
    source = Path(filename or "contacts_export.json")
    data = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("JSON must contain a list of contacts.")

    added = updated = skipped = errors = 0
    for number, raw in enumerate(data, 1):
        try:
            contact = validate_contact(raw)
            with database_cursor() as cur:
                ids = find_contact_ids(cur, contact["first_name"], contact["last_name"])
                if len(ids) > 1:
                    raise ValueError("Several existing contacts have the same full name.")

                if ids:
                    full_name = f"{contact['first_name']} {contact['last_name']}".strip()
                    choice = input(
                        f"{full_name} already exists. skip / overwrite? "
                    ).strip().lower()
                    if choice != "overwrite":
                        skipped += 1
                        continue
                    save_json_contact(cur, contact, ids[0])
                    updated += 1
                else:
                    save_json_contact(cur, contact)
                    added += 1
        except Exception as error:
            errors += 1
            print(f"Row {number} skipped: {error}")

    print(f"JSON import: {added} added, {updated} overwritten, "
          f"{skipped} skipped, {errors} errors.")


def import_csv():
    filename = input("CSV filename [contacts.csv]: ").strip()
    source = Path(filename or Path(__file__).with_name("contacts.csv"))
    added = updated = errors = 0

    with source.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {"first_name", "phone", "email", "birthday", "group"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("CSV needs first_name, phone, email, birthday, group columns.")
        if "phone_type" not in reader.fieldnames and "type" not in reader.fieldnames:
            raise ValueError("CSV needs a phone_type (or type) column.")

        for number, row in enumerate(reader, 2):
            raw = {
                "first_name": row.get("first_name"),
                "last_name": row.get("last_name"),
                "email": row.get("email"),
                "birthday": row.get("birthday"),
                "group": row.get("group") or "Other",
                "phones": [{
                    "phone": row.get("phone"),
                    "type": row.get("phone_type") or row.get("type") or "mobile",
                }],
            }
            try:
                contact = validate_contact(raw)
                with database_cursor() as cur:
                    ids = find_contact_ids(cur, contact["first_name"], contact["last_name"])
                    if len(ids) > 1:
                        raise ValueError("Several contacts have this full name.")

                    if ids:
                        contact_id = ids[0]
                        group_id = get_group_id(cur, contact["group"])
                        cur.execute(
                            "UPDATE contacts SET "
                            "email = COALESCE(%s, email), "
                            "birthday = COALESCE(%s, birthday), "
                            "group_id = %s WHERE id = %s",
                            (contact["email"], contact["birthday"], group_id, contact_id),
                        )
                        phone_item = contact["phones"][0]
                        cur.execute(
                            "SELECT contact_id FROM phones WHERE phone = %s",
                            (phone_item["phone"],),
                        )
                        owner = cur.fetchone()
                        if owner and owner[0] != contact_id:
                            raise ValueError("Phone belongs to another contact.")
                        cur.execute(
                            "INSERT INTO phones (contact_id, phone, type) "
                            "VALUES (%s, %s, %s) "
                            "ON CONFLICT (phone) DO UPDATE SET type = EXCLUDED.type",
                            (contact_id, phone_item["phone"], phone_item["type"]),
                        )
                        updated += 1
                    else:
                        save_json_contact(cur, contact)
                        added += 1
            except Exception as error:
                errors += 1
                print(f"CSV line {number} skipped: {error}")

    print(f"CSV import: {added} new contacts, {updated} existing rows, {errors} errors.")


def add_phone():
    full_name = input("Contact full name: ").strip()
    phone = input("New phone: ").strip()
    phone_type = input("Phone type (home/work/mobile): ").strip().lower()
    with database_cursor() as cur:
        cur.execute("CALL add_phone(%s, %s, %s)", (full_name, phone, phone_type))
    print("Phone saved.")


def move_to_group():
    full_name = input("Contact full name: ").strip()
    group_name = input("New group name: ").strip()
    with database_cursor() as cur:
        cur.execute("CALL move_to_group(%s, %s)", (full_name, group_name))
    print("Contact moved to group.")


def search_everywhere():
    query = input("Search name, surname, email, phone, group or birthday: ").strip()
    with database_cursor() as cur:
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        ids = [row[0] for row in cur.fetchall()]
        contacts = select_contacts(cur, "pb.id = ANY(%s)", (ids,)) if ids else []
    display_contacts(contacts)


def main():
    actions = {
        "1": filter_by_group,
        "2": search_by_email,
        "3": sort_contacts,
        "4": paginate_contacts,
        "5": export_json,
        "6": import_json,
        "7": import_csv,
        "8": add_phone,
        "9": move_to_group,
        "10": search_everywhere,
    }

    while True:
        print("\n--- TSIS 1 PHONEBOOK ---")
        print("1. Filter by group")
        print("2. Search by email")
        print("3. Sort contacts")
        print("4. Browse pages (next/prev/quit)")
        print("5. Export to JSON")
        print("6. Import from JSON")
        print("7. Import from extended CSV")
        print("8. Add a phone number")
        print("9. Move contact to a group")
        print("10. Search all fields")
        print("0. Exit")
        choice = input("Choose: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if not action:
            print("Invalid choice.")
            continue

        try:
            action()
        except Exception as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
