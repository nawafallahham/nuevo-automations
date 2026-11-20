// POST /api/lead — progress through the qualifying questions (js/calendly.js).
// The browser sends the whole state each time; the row only ever moves
// forward (a later beacon can't undo a decline or a booking).
import { json, readJson, clean, cleanOrNull, clientIp, ipHash, rateLimit, originAllowed } from './lib.js';

const ID_RE = /^ld_[a-f0-9]{16,40}$/;
const RANK = { started: 0, declined: 1, qualified: 1, details: 2, booked: 3 };

export async function lead(request, env) {
  if (!originAllowed(request)) return json({ ok: false, error: 'bad_origin' }, 403);
  const body = await readJson(request, 4096);
  const id = clean(body.id, 48);
  if (!ID_RE.test(id)) return json({ ok: false, error: 'bad_id' }, 400);

  const ua = request.headers.get('user-agent') || '';
  if (/bot|crawl|spider|slurp|headless|lighthouse|facebookexternalhit/i.test(ua)) return json({ ok: true });
  const ipH = await ipHash(env, clientIp(request));
  if (!(await rateLimit(env, 'lead:' + ipH, 120))) return json({ ok: false, error: 'rate_limited' }, 429);

  const status = Object.prototype.hasOwnProperty.call(RANK, body.status) && body.status !== 'booked' ? body.status : 'started';
  const answers = Array.isArray(body.answers) ? body.answers.slice(0, 4).map((a) => cleanOrNull(a, 80)) : [];
  while (answers.length < 4) answers.push(null);
  const step = answers.filter(Boolean).length;
  const declinedAt = status === 'declined' ? Math.min(Math.max(parseInt(body.declined_at_q, 10) || step, 1), 4) : null;
  const a = body.attribution && typeof body.attribution === 'object' ? body.attribution : {};
  const now = new Date().toISOString();

  await env.DB.prepare(
    'INSERT INTO leads (id, created_at, updated_at, page, status, step, q1, q2, q3, q4, declined_at_q, name, company, ' +
    'utm_source, utm_medium, utm_campaign, utm_content, landing, referrer, ip_hash) ' +
    'VALUES (?1, ?2, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15, ?16, ?17, ?18, ?19) ' +
    'ON CONFLICT (id) DO UPDATE SET updated_at = excluded.updated_at, ' +
    // status and answers only move forward
    "status = CASE WHEN leads.status IN ('declined', 'booked') THEN leads.status " +
    "  WHEN (CASE excluded.status WHEN 'details' THEN 2 WHEN 'qualified' THEN 1 WHEN 'declined' THEN 1 ELSE 0 END) >= " +
    "       (CASE leads.status WHEN 'details' THEN 2 WHEN 'qualified' THEN 1 ELSE 0 END) THEN excluded.status ELSE leads.status END, " +
    "step = CASE WHEN leads.status IN ('declined', 'booked') THEN leads.step ELSE MAX(leads.step, excluded.step) END, " +
    "q1 = CASE WHEN leads.status IN ('declined', 'booked') THEN leads.q1 ELSE COALESCE(excluded.q1, leads.q1) END, " +
    "q2 = CASE WHEN leads.status IN ('declined', 'booked') THEN leads.q2 ELSE COALESCE(excluded.q2, leads.q2) END, " +
    "q3 = CASE WHEN leads.status IN ('declined', 'booked') THEN leads.q3 ELSE COALESCE(excluded.q3, leads.q3) END, " +
    "q4 = CASE WHEN leads.status IN ('declined', 'booked') THEN leads.q4 ELSE COALESCE(excluded.q4, leads.q4) END, " +
    'declined_at_q = COALESCE(leads.declined_at_q, excluded.declined_at_q), ' +
    'name = COALESCE(excluded.name, leads.name), company = COALESCE(excluded.company, leads.company)'
  ).bind(
    id, now, cleanOrNull(body.page, 40), status, step, answers[0], answers[1], answers[2], answers[3], declinedAt,
    cleanOrNull(body.name, 100), cleanOrNull(body.company, 120),
    cleanOrNull(a.utm_source, 100), cleanOrNull(a.utm_medium, 100), cleanOrNull(a.utm_campaign, 150),
    cleanOrNull(a.utm_content, 150), cleanOrNull(a.landing, 300), cleanOrNull(a.referrer, 300), ipH
  ).run();
  return json({ ok: true });
}

// Called from the Calendly beacon: mark the lead booked.
export function markBooked(env, leadId, inviteeUri) {
  if (!ID_RE.test(String(leadId || ''))) return null;
  return env.DB.prepare(
    "UPDATE leads SET status = 'booked', invitee_uri = ?2, booked_at = COALESCE(booked_at, ?3), updated_at = ?3 WHERE id = ?1"
  ).bind(leadId, inviteeUri, new Date().toISOString());
}
