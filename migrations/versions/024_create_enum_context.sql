DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'context_enum') THEN
        CREATE TYPE context_enum AS ENUM (
			'pre-deal',
			'post-deal',
			'schedule',
			'manual',
			'bot',
			'balancing',
			'balance',
			'disbalance',
			'pre-balancing',
			'post-balancing',
			'bot-config-update'
        );
    END IF;
END$$;

