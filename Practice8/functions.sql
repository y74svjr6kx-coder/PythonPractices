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
    SELECT p.id, p.first_name, p.last_name, p.phone
    FROM phonebook AS p
    WHERE p.first_name ILIKE '%' || p_pattern || '%'
       OR p.last_name ILIKE '%' || p_pattern || '%'
       OR p.phone LIKE '%' || p_pattern || '%'
    ORDER BY p.id;
END;
$$;


CREATE OR REPLACE FUNCTION get_contacts_page(p_limit INTEGER, p_offset INTEGER)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20)
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_limit < 1 OR p_offset < 0
       OR p_limit IS NULL OR p_offset IS NULL THEN
        RAISE EXCEPTION 'Limit must be positive and offset cannot be negative';
    END IF;

    RETURN QUERY
    SELECT p.id, p.first_name, p.last_name, p.phone
    FROM phonebook AS p
    ORDER BY p.id
    LIMIT p_limit OFFSET p_offset;
END;
$$;
