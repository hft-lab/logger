DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'side_enum') THEN
        CREATE TYPE side_enum AS ENUM (
            'sell',
			'buy'
        );
    END IF;
END$$;