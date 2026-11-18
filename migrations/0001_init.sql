-- Nuevo site: bookings, anonymous analytics, rate limiting.

CREATE TABLE IF NOT EXISTS bookings (
  id            TEXT PRIMARY KEY,              -- 'bk_' + random
  date          TEXT NOT NULL,                 -- YYYY-MM-DD (Dubai)
  time          TEXT NOT NULL,                 -- HH:MM (Dubai)
  name          TEXT NOT NULL,
  phone         TEXT NOT NULL,
  business      TEXT NOT NULL,
  email         TEXT,
  note          TEXT,
  source        TEXT,
  utm_source    TEXT,
  utm_medium    TEXT,
  utm_campaign  TEXT,
  utm_content   TEXT,
  utm_term      TEXT,
  fbclid        TEXT,
  landing       TEXT,
  referrer      TEXT,
  status        TEXT NOT NULL DEFAULT 'booked', -- booked | cancelled
  created_at    TEXT NOT NULL,                 -- ISO UTC
  ip_hash       TEXT
);

-- One live booking per slot. Cancelled rows don't count, so a cancelled
-- slot can be re-booked. This is what makes double-booking impossible.
CREATE UNIQUE INDEX IF NOT EXISTS bookings_slot_live
  ON bookings (date, time) WHERE status = 'booked';
CREATE INDEX IF NOT EXISTS bookings_date ON bookings (date);
CREATE INDEX IF NOT EXISTS bookings_created ON bookings (created_at);

-- Anonymous first-party analytics. No cookies, no raw IP / UA:
-- visitor = truncated sha256(daily salt + ip + ua), so it can't be linked
-- across days or reversed.
CREATE TABLE IF NOT EXISTS events (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  ts            TEXT NOT NULL,                 -- ISO UTC
  type          TEXT NOT NULL,                 -- pageview | cta | book_view | book_start
  path          TEXT,
  ref_host      TEXT,
  utm_source    TEXT,
  utm_campaign  TEXT,
  visitor       TEXT
);
CREATE INDEX IF NOT EXISTS events_ts ON events (ts);
CREATE INDEX IF NOT EXISTS events_type ON events (type);

-- Fixed-window rate limiting: key = '<bucket>:<hash>', window = the current
-- window label (e.g. hour); count resets when the window changes.
CREATE TABLE IF NOT EXISTS rate (
  key           TEXT PRIMARY KEY,
  count         INTEGER NOT NULL DEFAULT 0,
  "window"      TEXT NOT NULL
);
