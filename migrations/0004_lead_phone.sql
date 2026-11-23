-- Name and WhatsApp number are asked before the qualifying questions
-- (js/calendly.js). capi_lead_at marks the Meta CAPI Lead event as sent,
-- so it goes out once per lead.
ALTER TABLE leads ADD COLUMN phone TEXT;
ALTER TABLE leads ADD COLUMN capi_lead_at TEXT;
