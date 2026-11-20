-- Qualifying questions before the booking calendar (js/calendly.js).
-- One row per visitor who starts the questions, updated as they go:
-- started -> declined | qualified -> details (name + company given) -> booked.
-- The nightly cron deletes rows after 180 days (privacy policy).

CREATE TABLE IF NOT EXISTS leads (
  id            TEXT PRIMARY KEY,              -- 'ld_' + random, made in the browser
  created_at    TEXT NOT NULL,                 -- ISO UTC
  updated_at    TEXT NOT NULL,
  page          TEXT,                          -- .cal-embed data-source: wellness-landing | meta-landing | site
  status        TEXT NOT NULL DEFAULT 'started',
  step          INTEGER NOT NULL DEFAULT 0,    -- questions answered
  q1            TEXT,                          -- role
  q2            TEXT,                          -- orders a week
  q3            TEXT,                          -- average order value
  q4            TEXT,                          -- Meta ads today
  declined_at_q INTEGER,                       -- the question whose answer declined them
  name          TEXT,
  company       TEXT,
  invitee_uri   TEXT,                          -- Calendly invitee, once booked
  booked_at     TEXT,
  utm_source    TEXT,
  utm_medium    TEXT,
  utm_campaign  TEXT,
  utm_content   TEXT,
  landing       TEXT,
  referrer      TEXT,
  ip_hash       TEXT
);
CREATE INDEX IF NOT EXISTS leads_created ON leads (created_at);
CREATE INDEX IF NOT EXISTS leads_invitee ON leads (invitee_uri);
