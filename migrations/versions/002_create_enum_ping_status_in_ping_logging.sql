DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'ping_status_enum') THEN
        CREATE TYPE ping_status_enum AS ENUM (
            'success',
			'no_connection'
        );
    END IF;
END$$;