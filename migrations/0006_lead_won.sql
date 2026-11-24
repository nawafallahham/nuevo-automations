-- "Won client" from the dashboard: won_at and won_value (AED) are set when
-- a lead signs; capi_won_at marks the Meta Purchase event as sent, so it
-- goes out once per lead (worker/admin.js).
ALTER TABLE leads ADD COLUMN won_at TEXT;
ALTER TABLE leads ADD COLUMN won_value REAL;
ALTER TABLE leads ADD COLUMN capi_won_at TEXT;
