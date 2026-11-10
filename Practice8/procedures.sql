CREATE OR REPLACE PROCEDURE upsert_contact(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id INTEGER;
BEGIN
    IF NULLIF(BTRIM(p_first_name), '') IS NULL THEN
        RAISE EXCEPTION 'First name is required';
    END IF;

    IF p_phone IS NULL OR p_phone !~ '^\+?[0-9]{10,15}$' THEN
        RAISE EXCEPTION 'Invalid phone number';
    END IF;

    SELECT p.id INTO v_id
    FROM phonebook AS p
    WHERE LOWER(p.first_name) = LOWER(BTRIM(p_first_name))
      AND LOWER(p.last_name) = LOWER(BTRIM(COALESCE(p_last_name, '')))
    ORDER BY p.id
    LIMIT 1;

    IF v_id IS NOT NULL THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE id = v_id;
    ELSE
        INSERT INTO phonebook (first_name, last_name, phone)
        VALUES (
            BTRIM(p_first_name),
            BTRIM(COALESCE(p_last_name, '')),
            p_phone
        );
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    IN p_contacts JSONB,
    INOUT p_invalid JSONB
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact JSONB;
    v_first_name TEXT;
    v_last_name TEXT;
    v_phone TEXT;
BEGIN
    IF p_contacts IS NULL OR jsonb_typeof(p_contacts) <> 'array' THEN
        RAISE EXCEPTION 'Contacts must be a JSON array';
    END IF;

    p_invalid := '[]'::JSONB;

    FOR v_contact IN
        SELECT value FROM jsonb_array_elements(p_contacts)
    LOOP
        v_first_name := BTRIM(COALESCE(v_contact->>'first_name', ''));
        v_last_name := BTRIM(COALESCE(v_contact->>'last_name', ''));
        v_phone := BTRIM(COALESCE(v_contact->>'phone', ''));

        IF v_first_name = ''
           OR v_phone !~ '^\+?[0-9]{10,15}$' THEN

            p_invalid := p_invalid || jsonb_build_array(
                jsonb_build_object(
                    'contact', v_contact,
                    'reason', 'Invalid name or phone'
                )
            );

        ELSE
            BEGIN
                CALL upsert_contact(
                    v_first_name::VARCHAR,
                    v_last_name::VARCHAR,
                    v_phone::VARCHAR
                );

            EXCEPTION
                WHEN unique_violation OR string_data_right_truncation THEN
                    p_invalid := p_invalid || jsonb_build_array(
                        jsonb_build_object(
                            'contact', v_contact,
                            'reason', SQLERRM
                        )
                    );
            END;
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(
    p_first_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NULLIF(BTRIM(COALESCE(p_phone, '')), '') IS NOT NULL THEN

        DELETE FROM phonebook
        WHERE phone = BTRIM(p_phone);

    ELSIF NULLIF(BTRIM(COALESCE(p_first_name, '')), '') IS NOT NULL THEN

        DELETE FROM phonebook
        WHERE LOWER(first_name) = LOWER(BTRIM(p_first_name));

    ELSE
        RAISE EXCEPTION 'Provide a name or a phone';
    END IF;
END;
$$;
