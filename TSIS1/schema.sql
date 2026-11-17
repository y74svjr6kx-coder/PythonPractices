BEGIN;

ALTER TABLE phonebook
ADD COLUMN IF NOT EXISTS last_name VARCHAR(100) NOT NULL DEFAULT '';

CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO groups (name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;

CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY REFERENCES phonebook(id) ON DELETE CASCADE,
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES groups(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) UNIQUE NOT NULL,
    type VARCHAR(10) NOT NULL CHECK (type IN ('home', 'work', 'mobile'))
);

CREATE INDEX IF NOT EXISTS phones_contact_id_idx ON phones (contact_id);
CREATE INDEX IF NOT EXISTS contacts_group_id_idx ON contacts (group_id);

INSERT INTO contacts (id, group_id)
SELECT pb.id, g.id
FROM phonebook AS pb
CROSS JOIN groups AS g
WHERE g.name = 'Other'
ON CONFLICT (id) DO NOTHING;

UPDATE contacts
SET group_id = (SELECT id FROM groups WHERE name = 'Other')
WHERE group_id IS NULL;

INSERT INTO phones (contact_id, phone, type)
SELECT pb.id, pb.phone, 'mobile'
FROM phonebook AS pb
WHERE pb.phone IS NOT NULL AND BTRIM(pb.phone) <> ''
ON CONFLICT (phone) DO NOTHING;

COMMIT;
