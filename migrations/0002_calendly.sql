-- Calendly becomes the scheduler. Calendly bookings land in the same
-- bookings table (provider = 'calendly') so the dashboard, calendar feed,
-- email alerts, OrcaFlo hook and Meta CAPI keep working unchanged.

ALTER TABLE bookings ADD COLUMN calendly_invitee_uri TEXT;   -- https://api.calendly.com/scheduled_events/…/invitees/…
ALTER TABLE bookings ADD COLUMN calendly_event_uri   TEXT;   -- https://api.calendly.com/scheduled_events/…
ALTER TABLE bookings ADD COLUMN cancel_url           TEXT;
ALTER TABLE bookings ADD COLUMN reschedule_url       TEXT;
ALTER TABLE bookings ADD COLUMN provider             TEXT DEFAULT 'native'; -- native | calendly
ALTER TABLE bookings ADD COLUMN capi_sent_at         TEXT;   -- ISO UTC; Calendly CAPI step runs at most once

-- Webhook idempotency: one row per Calendly invitee (NULLs don't collide).
CREATE UNIQUE INDEX IF NOT EXISTS bookings_calendly_invitee ON bookings (calendly_invitee_uri);

-- Calendly owns availability for its rows, so the one-live-booking-per-slot
-- rule only applies to native bookings now.
DROP INDEX IF EXISTS bookings_slot_live;
CREATE UNIQUE INDEX IF NOT EXISTS bookings_slot_live
  ON bookings (date, time) WHERE status = 'booked' AND provider = 'native';

-- What the browser knows about a Calendly booking (consent, attribution,
-- Meta click ids, and ip/ua only when consent was given), keyed by invitee
-- uri. Written by POST /api/calendly/scheduled; the webhook and the beacon
-- can arrive in either order. ip/ua are cleared once the CAPI step has run
-- and the nightly cron deletes rows after 2 days.
CREATE TABLE IF NOT EXISTS calendly_pending (
  invitee_uri   TEXT PRIMARY KEY,
  data          TEXT,                          -- JSON
  created_at    TEXT                           -- ISO UTC
);
