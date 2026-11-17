CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_count INTEGER;
    v_phone TEXT := BTRIM(COALESCE(p_phone, ''));
    v_type TEXT := LOWER(BTRIM(COALESCE(p_type, '')));
BEGIN
    IF NULLIF(BTRIM(COALESCE(p_contact_name, '')), '') IS NULL THEN
        RAISE EXCEPTION 'Contact name is required';
    END IF;

    IF v_phone !~ '^\+?[0-9]{10,15}$' THEN
        RAISE EXCEPTION 'Phone must have 10-15 digits and an optional leading +';
    END IF;

    IF v_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Phone type must be home, work or mobile';
    END IF;

    SELECT COUNT(*), MIN(pb.id)
    INTO v_count, v_contact_id
    FROM phonebook AS pb
    JOIN contacts AS c ON c.id = pb.id
    WHERE LOWER(BTRIM(CONCAT_WS(' ', pb.first_name, NULLIF(pb.last_name, ''))))
        = LOWER(BTRIM(p_contact_name));

    IF v_count = 0 THEN
        RAISE EXCEPTION 'Contact not found: %', p_contact_name;
    ELSIF v_count > 1 THEN
        RAISE EXCEPTION 'Several contacts have this name. Use a unique full name';
    END IF;

    IF EXISTS (
        SELECT 1 FROM phones
        WHERE phone = v_phone AND contact_id <> v_contact_id
    ) THEN
        RAISE EXCEPTION 'Phone already belongs to another contact';
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, v_phone, v_type)
    ON CONFLICT (phone) DO UPDATE SET type = EXCLUDED.type
    WHERE phones.contact_id = EXCLUDED.contact_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Phone already belongs to another contact';
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_count INTEGER;
    v_group_id INTEGER;
    v_group_name TEXT := INITCAP(BTRIM(COALESCE(p_group_name, '')));
BEGIN
    IF NULLIF(BTRIM(COALESCE(p_contact_name, '')), '') IS NULL THEN
        RAISE EXCEPTION 'Contact name is required';
    END IF;

    IF v_group_name = '' OR LENGTH(v_group_name) > 50 THEN
        RAISE EXCEPTION 'Group name must have 1-50 characters';
    END IF;

    SELECT COUNT(*), MIN(pb.id)
    INTO v_count, v_contact_id
    FROM phonebook AS pb
    JOIN contacts AS c ON c.id = pb.id
    WHERE LOWER(BTRIM(CONCAT_WS(' ', pb.first_name, NULLIF(pb.last_name, ''))))
        = LOWER(BTRIM(p_contact_name));

    IF v_count = 0 THEN
        RAISE EXCEPTION 'Contact not found: %', p_contact_name;
    ELSIF v_count > 1 THEN
        RAISE EXCEPTION 'Several contacts have this name. Use a unique full name';
    END IF;

    INSERT INTO groups (name)
    VALUES (v_group_name)
    ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
    RETURNING id INTO v_group_id;

    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(p_pattern TEXT)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.first_name, pb.last_name, pb.phone
    FROM phonebook AS pb
    LEFT JOIN contacts AS c ON c.id = pb.id
    LEFT JOIN groups AS g ON g.id = c.group_id
    WHERE pb.first_name ILIKE '%' || p_pattern || '%'
       OR pb.last_name ILIKE '%' || p_pattern || '%'
       OR pb.phone ILIKE '%' || p_pattern || '%'
       OR c.email ILIKE '%' || p_pattern || '%'
       OR g.name ILIKE '%' || p_pattern || '%'
       OR c.birthday::TEXT LIKE '%' || p_pattern || '%'
       OR EXISTS (
           SELECT 1
           FROM phones AS ph
           WHERE ph.contact_id = pb.id
             AND ph.phone ILIKE '%' || p_pattern || '%'
       )
    ORDER BY pb.id;
END;
$$;
