-- capi_qual_at marks the Meta SubmitApplication event (qualified lead) as
-- sent, so it goes out once per lead (worker/leads.js).
ALTER TABLE leads ADD COLUMN capi_qual_at TEXT;
