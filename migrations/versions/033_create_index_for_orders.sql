BEGIN;

LOCK orders IN ROW EXCLUSIVE MODE NOWAIT;

CREATE INDEX ix_orders_exchange_exchange_order_id ON orders USING btree (exchange, exchange_order_id);
CREATE INDEX ix_orders_exchange_id ON orders USING btree (id);
CREATE INDEX ix_orders_datetime ON orders USING btree (datetime);
CREATE INDEX ix_orders_context ON orders USING btree (context);
CREATE INDEX ix_orders_parent_id ON orders USING btree (parent_id);
CREATE INDEX ix_orders_status ON orders USING btree (status);
CREATE INDEX ix_orders_expect_price ON orders USING btree (expect_price);

COMMIT;