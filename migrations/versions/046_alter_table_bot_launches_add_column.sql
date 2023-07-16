BEGIN;

LOCK bot_launches IN ROW EXCLUSIVE MODE NOWAIT;

ALTER TABLE bot_launches add column shift_use_flag INT;
ALTER TABLE bot_launches add column bot_config_id UUID;
ALTER TABLE bot_launches add column updated_flag INT;
ALTER TABLE bot_launches add column datetime_update timestamptz;
ALTER TABLE bot_launches add column ts_update BIGINT;

COMMIT;
