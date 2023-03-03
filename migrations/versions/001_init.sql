CREATE TABLE IF NOT EXISTS "migration"
(
    id SERIAL PRIMARY KEY NOT NULL,
    migration_name VARCHAR(255) NOT NULL UNIQUE,
    created timestamptz NOT NULL
);