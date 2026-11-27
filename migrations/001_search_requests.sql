CREATE TABLE IF NOT EXISTS search_requests (
    id         SERIAL PRIMARY KEY,
    chat_id    BIGINT NOT NULL,
    city_from  TEXT NOT NULL,
    city_to    TEXT NOT NULL,
    trip_date  DATE NOT NULL,
    time_from  TIME,
    time_to    TIME,
    status     TEXT NOT NULL DEFAULT 'active'
               CHECK (status IN ('active', 'found', 'closed', 'expired')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    closed_at  TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS search_requests_active_idx
    ON search_requests (chat_id)
    WHERE status IN ('active', 'found');
