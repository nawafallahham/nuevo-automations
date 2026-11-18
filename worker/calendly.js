// Calendly integration. Calendly is the scheduler; every booking it makes is
// copied into the bookings table (provider = 'calendly') so the dashboard,
// calendar feed, email alert and OrcaFlo hook work exactly as for a native
// booking.
//
//   POST /api/calendly/webhook        invitee.created / invitee.canceled (signed by Calendly)
//   POST /api/calendly/scheduled      browser beacon from js/calendly.js (consent + attribution)
//   POST /api/admin/calendly/setup    (re)create our webhook subscription with CALENDLY_TOKEN
//   GET  /api/admin/calendly/status   secrets set? current subscriptions for our URL
//
// Meta CAPI needs the visitor's consent, IP and browser, which only the
// browser beacon knows. Webhook and beacon can arrive in either order, so
// both call capiStep() after their own write; whichever lands second finds
// both halves, and an atomic claim on capi_sent_at makes it send once.
import {
  json, noContent, readJson, clean, cleanOrNull, hostOf, randomId, clientIp, ipHash,
  rateLimit, originAllowed, safeEqual, dubaiNow, HttpError
} from './lib.js';
import { runSideEffects, sendMetaCapi, sendCancelNotice, fetchWithTimeout } from './notify.js';

const CAL_API = 'https://api.calendly.com';
const INVITEE_RE = /^https:\/\/api\.calendly\.com\/scheduled_events\/[\w-]{1,64}\/invitees\/[\w-]{1,64}$/;
const SIG_MAX_AGE_S = 5 * 60;
const enc = new TextEncoder();

function siteUrl(env) { return env.SITE_URL || 'https://nuevoautomations.com'; }
function callbackUrl(env) { return siteUrl(env) + '/api/calendly/webhook'; }

function parseJson(s) {
  try { const v = JSON.parse(s || 'null'); return v && typeof v === 'object' ? v : null; } catch (e) { return null; }
}

// ---- Signature --------------------------------------------------------------
// Calendly-Webhook-Signature: t=<unix seconds>,v1=<hex HMAC-SHA256(key, t + '.' + body)>
export async function verifySignature(key, header, rawBody, now = Date.now()) {
  if (!key || !header) return false;
  const parts = {};
  for (const kv of String(header).split(',')) {
    const i = kv.indexOf('=');
    if (i > 0) parts[kv.slice(0, i).trim()] = kv.slice(i + 1).trim();
  }
  const t = Number(parts.t);
  if (!/^\d{1,12}$/.test(parts.t || '') || !/^[a-f0-9]{64}$/i.test(parts.v1 || '')) return false;
  if (Math.abs(now / 1000 - t) > SIG_MAX_AGE_S) return false;
  const k = await crypto.subtle.importKey('raw', enc.encode(key), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const mac = await crypto.subtle.sign('HMAC', k, enc.encode(parts.t + '.' + rawBody));
  const hex = [...new Uint8Array(mac)].map((b) => b.toString(16).padStart(2, '0')).join('');
  return safeEqual(hex, parts.v1.toLowerCase());
}

async function readRaw(request, maxBytes) {
  if (Number(request.headers.get('content-length') || 0) > maxBytes) throw new HttpError(413, 'too_large');
  const text = await request.text();
  if (text.length > maxBytes) throw new HttpError(413, 'too_large');
  return text;
}

// ---- POST /api/calendly/webhook ---------------------------------------------
export async function webhook(request, env, ctx) {
  if (!env.CALENDLY_SIGNING_KEY) return json({ ok: false, error: 'not_configured' }, 503);
  const raw = await readRaw(request, 65536);
  if (!(await verifySignature(env.CALENDLY_SIGNING_KEY, request.headers.get('calendly-webhook-signature'), raw))) {
    return json({ ok: false, error: 'bad_signature' }, 401);
  }
  const body = parseJson(raw);
  if (!body) return json({ ok: false, error: 'bad_json' }, 400);
  const p = body.payload && typeof body.payload === 'object' ? body.payload : {};
  const inviteeUri = clean(p.uri, 300);
  if (!INVITEE_RE.test(inviteeUri)) return json({ ok: false, error: 'bad_invitee' }, 400);

  if (body.event === 'invitee.created') return created(env, ctx, p, inviteeUri);
  if (body.event === 'invitee.canceled') return canceled(env, ctx, p, inviteeUri);
  return json({ ok: true, ignored: clean(body.event, 60) }); // 2xx so Calendly doesn't retry
}

// Calendly's Q&A -> phone / business / note. The first question that looks
// like a phone (or business) question supplies that field; everything else
// is kept as the note.
function mapAnswers(qas) {
  const list = (Array.isArray(qas) ? qas : [])
    .map((q) => ({ q: clean(q && q.question, 200), a: clean(q && q.answer, 400) }))
    .filter((x) => x.a);
  const phoneAt = list.findIndex((x) => /whatsapp|phone|mobile/i.test(x.q));
  const bizAt = list.findIndex((x, i) => i !== phoneAt && /business|company/i.test(x.q));
  return {
    phone: phoneAt >= 0 ? list[phoneAt].a.slice(0, 32) : '',
    business: bizAt >= 0 ? list[bizAt].a.slice(0, 80) : '',
    note: list.filter((x, i) => i !== phoneAt && i !== bizAt).map((x) => x.q + ': ' + x.a).join(' · ').slice(0, 1000)
  };
}

async function pendingFor(env, inviteeUri) {
  const row = await env.DB.prepare('SELECT data FROM calendly_pending WHERE invitee_uri = ?1').bind(inviteeUri).first();
  return row ? parseJson(row.data) || {} : null;
}

async function created(env, ctx, p, inviteeUri) {
  const se = p.scheduled_event && typeof p.scheduled_event === 'object' ? p.scheduled_event : {};
  const startMs = Date.parse(se.start_time);
  if (isNaN(startMs)) return json({ ok: false, error: 'bad_start_time' }, 400);
  const dubai = dubaiNow(startMs).toISOString(); // Asia/Dubai wall time (UTC+4, no DST)

  const pending = await pendingFor(env, inviteeUri);
  const a = (pending && pending.attribution) || {};
  const tr = p.tracking && typeof p.tracking === 'object' ? p.tracking : {};
  const qa = mapAnswers(p.questions_and_answers);
  const email = clean(p.email, 120).toLowerCase();
  const name = clean(p.name, 80) || clean([p.first_name, p.last_name].filter(Boolean).join(' '), 80) || email || 'Calendly invitee';

  const b = {
    id: randomId('bk_'),
    date: dubai.slice(0, 10),
    time: dubai.slice(11, 16),
    name,
    phone: qa.phone || clean(p.text_reminder_number, 32),
    business: qa.business,
    email: email || null,
    note: qa.note || null,
    source: (pending && cleanOrNull(pending.source, 40)) || 'calendly',
    utm_source: cleanOrNull(tr.utm_source || a.utm_source, 100),
    utm_medium: cleanOrNull(tr.utm_medium || a.utm_medium, 100),
    utm_campaign: cleanOrNull(tr.utm_campaign || a.utm_campaign, 150),
    utm_content: cleanOrNull(tr.utm_content || a.utm_content, 150),
    utm_term: cleanOrNull(tr.utm_term || a.utm_term, 150),
    fbclid: cleanOrNull(a.fbclid, 500),
    landing: cleanOrNull(a.landing, 300),
    referrer: cleanOrNull(a.referrer, 300),
    created_at: new Date().toISOString(),
    ip_hash: null,
    provider: 'calendly',
    calendly_invitee_uri: inviteeUri,
    calendly_event_uri: cleanOrNull(se.uri, 300),
    cancel_url: cleanOrNull(p.cancel_url, 300),
    reschedule_url: cleanOrNull(p.reschedule_url, 300)
  };

  // Idempotent on the invitee uri: Calendly retries, and a replay must not
  // send a second alert.
  const r = await env.DB.prepare(
    'INSERT INTO bookings (id, date, time, name, phone, business, email, note, source, ' +
    'utm_source, utm_medium, utm_campaign, utm_content, utm_term, fbclid, landing, referrer, ' +
    'status, created_at, ip_hash, provider, calendly_invitee_uri, calendly_event_uri, cancel_url, reschedule_url) ' +
    "VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15, ?16, ?17, 'booked', ?18, ?19, ?20, ?21, ?22, ?23, ?24) " +
    'ON CONFLICT (calendly_invitee_uri) DO NOTHING'
  ).bind(
    b.id, b.date, b.time, b.name, b.phone, b.business, b.email, b.note, b.source,
    b.utm_source, b.utm_medium, b.utm_campaign, b.utm_content, b.utm_term, b.fbclid, b.landing, b.referrer,
    b.created_at, b.ip_hash, b.provider, b.calendly_invitee_uri, b.calendly_event_uri, b.cancel_url, b.reschedule_url
  ).run();
  if (!((r.meta && r.meta.changes) || 0)) return json({ ok: true, duplicate: true });

  // Email + OrcaFlo now. CAPI is left to capiStep (consent: false here),
  // because only the browser beacon knows whether the visitor consented.
  runSideEffects(env, ctx, b, { consent: false });
  runCapiStep(env, ctx, inviteeUri);
  return json({ ok: true, id: b.id, date: b.date, time: b.time });
}

async function canceled(env, ctx, p, inviteeUri) {
  // A reschedule is a cancel of this invitee plus a fresh invitee.created
  // for the new time, so both cases just cancel this row.
  const b = await env.DB.prepare(
    "UPDATE bookings SET status = 'cancelled' WHERE calendly_invitee_uri = ?1 AND status = 'booked' RETURNING *"
  ).bind(inviteeUri).first();
  if (!b) return json({ ok: true, changed: false });
  const reason = clean(p.cancellation && p.cancellation.reason, 300);
  ctx.waitUntil(
    sendCancelNotice(env, b, p.rescheduled === true, reason)
      .catch((err) => console.error('[email] ' + b.id + ' cancel notice: ' + (err && err.message || err)))
  );
  return json({ ok: true, id: b.id, status: 'cancelled' });
}

// ---- POST /api/calendly/scheduled (browser beacon) ---------------------------
export async function scheduledBeacon(request, env, ctx) {
  if (!originAllowed(request)) return json({ ok: false, error: 'bad_origin' }, 403);
  const body = await readJson(request, 8192);
  const ip = clientIp(request);
  if (!(await rateLimit(env, 'calendly:' + (await ipHash(env, ip)), 10))) {
    return json({ ok: false, error: 'rate_limited' }, 429, { 'Retry-After': '3600' });
  }

  const inviteeUri = clean(body.invitee_uri, 300);
  if (!inviteeUri.startsWith(CAL_API + '/') || !INVITEE_RE.test(inviteeUri)) {
    return json({ ok: false, error: 'bad_invitee' }, 400);
  }
  const eventUri = clean(body.event_uri, 300);
  const consent = body.consent === true;
  const a = body.attribution && typeof body.attribution === 'object' ? body.attribution : {};
  const attribution = {
    utm_source: cleanOrNull(a.utm_source, 100),
    utm_medium: cleanOrNull(a.utm_medium, 100),
    utm_campaign: cleanOrNull(a.utm_campaign, 150),
    utm_content: cleanOrNull(a.utm_content, 150),
    utm_term: cleanOrNull(a.utm_term, 150),
    fbclid: cleanOrNull(a.fbclid, 500),
    landing: cleanOrNull(a.landing, 300),
    referrer: cleanOrNull(a.referrer, 300)
  };
  const pageUrl = clean(body.page_url, 300);
  const data = {
    consent,
    source: cleanOrNull(body.source, 40),
    event_uri: eventUri.startsWith(CAL_API + '/') ? eventUri : null,
    page_url: hostOf(pageUrl) === hostOf(siteUrl(env)) ? pageUrl : siteUrl(env) + '/book/',
    attribution
  };
  // Meta matching data is only kept when the visitor accepted cookies, and
  // ip/ua are wiped again once the CAPI step has run.
  if (consent) {
    let fbc = clean(a.fbc, 500);
    if (!fbc && attribution.fbclid) fbc = 'fb.1.' + Date.now() + '.' + attribution.fbclid;
    data.fbc = fbc || null;
    data.fbp = clean(a.fbp, 200) || null;
    data.ip = ip;
    data.ua = clean(request.headers.get('user-agent'), 400);
  }

  await env.DB.batch([
    env.DB.prepare(
      'INSERT INTO calendly_pending (invitee_uri, data, created_at) VALUES (?1, ?2, ?3) ' +
      'ON CONFLICT (invitee_uri) DO UPDATE SET data = excluded.data'
    ).bind(inviteeUri, JSON.stringify(data), new Date().toISOString()),
    // Webhook got here first: fill in the attribution it couldn't know.
    env.DB.prepare(
      "UPDATE bookings SET source = CASE WHEN source IS NULL OR source = 'calendly' THEN COALESCE(?2, source) ELSE source END, " +
      'utm_source = COALESCE(utm_source, ?3), utm_medium = COALESCE(utm_medium, ?4), utm_campaign = COALESCE(utm_campaign, ?5), ' +
      'utm_content = COALESCE(utm_content, ?6), utm_term = COALESCE(utm_term, ?7), fbclid = COALESCE(fbclid, ?8), ' +
      'landing = COALESCE(landing, ?9), referrer = COALESCE(referrer, ?10) WHERE calendly_invitee_uri = ?1'
    ).bind(
      inviteeUri, data.source, attribution.utm_source, attribution.utm_medium, attribution.utm_campaign,
      attribution.utm_content, attribution.utm_term, attribution.fbclid, attribution.landing, attribution.referrer
    )
  ]);

  runCapiStep(env, ctx, inviteeUri);
  return noContent();
}

// ---- Meta CAPI, once both halves are in --------------------------------------
function runCapiStep(env, ctx, inviteeUri) {
  ctx.waitUntil(
    capiStep(env, inviteeUri).catch((err) => console.error('[meta_capi] ' + inviteeUri + ': ' + (err && err.message || err)))
  );
}

async function capiStep(env, inviteeUri) {
  const [bkRes, pendRes] = await env.DB.batch([
    env.DB.prepare('SELECT * FROM bookings WHERE calendly_invitee_uri = ?1').bind(inviteeUri),
    env.DB.prepare('SELECT data FROM calendly_pending WHERE invitee_uri = ?1').bind(inviteeUri)
  ]);
  const b = bkRes.results && bkRes.results[0];
  const pend = pendRes.results && pendRes.results[0];
  if (!b || !pend) return; // the other half will call us again
  const d = parseJson(pend.data) || {};
  if (d.consent !== true) return;
  if (b.capi_sent_at) { if (d.ip || d.ua) await wipeIpUa(env, inviteeUri); return; } // a repeat beacon re-stored them

  // Atomic claim: only one of webhook / beacon gets changes = 1.
  const claim = await env.DB.prepare(
    'UPDATE bookings SET capi_sent_at = ?2 WHERE calendly_invitee_uri = ?1 AND capi_sent_at IS NULL'
  ).bind(inviteeUri, new Date().toISOString()).run();
  if (!((claim.meta && claim.meta.changes) || 0)) return;

  const live = Boolean(env.META_CAPI_TOKEN && env.META_PIXEL_ID);
  console.log('[calendly] capi ' + b.id + (live ? ' sending' : ' skipped: META_CAPI_TOKEN not set'));
  try {
    await sendMetaCapi(env, b, {
      consent: true,
      event_id: inviteeUri, // same eventID as the browser pixel -> deduplicated
      ip: d.ip || null,
      ua: d.ua || '',
      fbc: d.fbc || null,
      fbp: d.fbp || null,
      page_url: d.page_url || siteUrl(env) + '/book/'
    });
  } finally {
    await wipeIpUa(env, inviteeUri);
  }
}

function wipeIpUa(env, inviteeUri) {
  return env.DB.prepare("UPDATE calendly_pending SET data = json_remove(data, '$.ip', '$.ua') WHERE invitee_uri = ?1")
    .bind(inviteeUri).run();
}

// ---- Admin: webhook subscription ------------------------------------------------
// The token is only ever sent to api.calendly.com and never logged.
async function cal(env, method, pathOrUrl, body) {
  const url = pathOrUrl.startsWith(CAL_API + '/') ? pathOrUrl : CAL_API + pathOrUrl;
  if (!url.startsWith(CAL_API + '/')) throw new Error('refusing non-Calendly url');
  const r = await fetchWithTimeout(url, {
    method,
    headers: { Authorization: 'Bearer ' + env.CALENDLY_TOKEN, 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined
  }, 10000);
  const text = await r.text();
  return { ok: r.ok, status: r.status, data: parseJson(text) || (text ? { raw: text.slice(0, 500) } : null) };
}

function calError(step, r) {
  const d = r.data || {};
  return json({
    ok: false,
    error: 'calendly_' + step + '_failed',
    message: 'Calendly ' + step + ' failed (' + r.status + '): ' + (d.message || d.title || 'no message'),
    status: r.status,
    calendly: d
  }, 502);
}

// Our user + organisation, then the subscriptions that point at our URL.
async function ourSubscriptions(env) {
  const me = await cal(env, 'GET', '/users/me');
  if (!me.ok) return { error: calError('users_me', me) };
  const user = me.data && me.data.resource && me.data.resource.uri;
  const organization = me.data && me.data.resource && me.data.resource.current_organization;
  const q = '?organization=' + encodeURIComponent(organization) + '&user=' + encodeURIComponent(user) + '&scope=user&count=100';
  const list = await cal(env, 'GET', '/webhook_subscriptions' + q);
  if (!list.ok) return { error: calError('list_subscriptions', list) };
  const subs = ((list.data && list.data.collection) || []).filter((s) => s && s.callback_url === callbackUrl(env));
  return { user, organization, subs };
}

function subView(s) {
  return { uri: s.uri, state: s.state, events: s.events, scope: s.scope, callback_url: s.callback_url, created_at: s.created_at };
}

export async function calendlySetup(env) {
  if (!env.CALENDLY_TOKEN) return json({ ok: false, error: 'calendly_token_not_set', message: 'Set the CALENDLY_TOKEN secret first.' }, 503);
  if (!env.CALENDLY_SIGNING_KEY) return json({ ok: false, error: 'calendly_signing_key_not_set', message: 'Set the CALENDLY_SIGNING_KEY secret first.' }, 503);

  const cur = await ourSubscriptions(env);
  if (cur.error) return cur.error;
  // Replace rather than reuse: an old subscription may carry an old signing key.
  for (const s of cur.subs) {
    const del = await cal(env, 'DELETE', s.uri);
    if (!del.ok && del.status !== 404) return calError('delete_subscription', del);
  }
  const made = await cal(env, 'POST', '/webhook_subscriptions', {
    url: callbackUrl(env),
    events: ['invitee.created', 'invitee.canceled'],
    organization: cur.organization,
    user: cur.user,
    scope: 'user',
    signing_key: env.CALENDLY_SIGNING_KEY
  });
  if (!made.ok) return calError('create_subscription', made);
  const s = (made.data && made.data.resource) || {};
  return json({ ok: true, removed: cur.subs.length, subscription: subView(s) });
}

export async function calendlyStatus(env) {
  const out = {
    ok: true,
    token_set: Boolean(env.CALENDLY_TOKEN),
    signing_key_set: Boolean(env.CALENDLY_SIGNING_KEY),
    callback_url: callbackUrl(env),
    subscriptions: []
  };
  if (!env.CALENDLY_TOKEN) return json(out);
  const cur = await ourSubscriptions(env);
  if (cur.error) {
    const e = await cur.error.json();
    return json({ ...out, error: e.message });
  }
  out.subscriptions = cur.subs.map(subView);
  return json(out);
}
