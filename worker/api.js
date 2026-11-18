// Public API: slots, booking, tracking, calendar feed.
import {
  json, noContent, readJson, clean, cleanOrNull, hostOf,
  dubaiToday, addDays, slotError, randomId, clientIp, ipHash, visitorHash,
  rateLimit, originAllowed, safeEqual
} from './lib.js';
import { runSideEffects } from './notify.js';
import { calendar, internalEvent } from './ics.js';

const EMAIL_RE = /^[^\s@<>()",;:]+@[^\s@<>()",;:]+\.[^\s@<>()",;:]{2,}$/;

// GET /api/slots?days=14 -> { ok, today, taken: { 'YYYY-MM-DD': ['14:00', ...] } }
// Only booked times, never customer details.
export async function slots(request, env) {
  const url = new URL(request.url);
  const days = Math.min(Math.max(parseInt(url.searchParams.get('days'), 10) || 14, 1), 30);
  const today = dubaiToday();
  try {
    const { results } = await env.DB.prepare(
      "SELECT date, time FROM bookings WHERE status = 'booked' AND date >= ?1 AND date <= ?2 ORDER BY date, time"
    ).bind(today, addDays(today, days - 1)).all();
    const taken = {};
    for (const r of results) (taken[r.date] = taken[r.date] || []).push(r.time);
    return json({ ok: true, today, taken });
  } catch (err) {
    console.error('[slots] ' + err.message);
    return json({ ok: false, reason: 'error', today, taken: {} });
  }
}

// POST /api/book
export async function book(request, env, ctx) {
  if (!originAllowed(request)) return json({ ok: false, error: 'bad_origin' }, 403);
  const body = await readJson(request, 8192);

  const ip = clientIp(request);
  const ipH = await ipHash(env, ip);

  // Count every attempt (valid or not) against the per-IP hourly budget.
  if (!(await rateLimit(env, 'book:' + ipH, 5))) {
    return json({ ok: false, error: 'rate_limited' }, 429, { 'Retry-After': '3600' });
  }

  const date = clean(body.date, 10);
  const time = clean(body.time, 5);

  // Honeypot: bots fill every field. Pretend it worked, store nothing.
  if (clean(body.website, 200)) {
    return json({ ok: true, id: randomId('bk_'), date, time });
  }

  const name = clean(body.name, 80);
  const phone = clean(body.phone, 32);
  const business = clean(body.business, 80);
  const email = clean(body.email, 120).toLowerCase();
  const note = clean(body.note, 400);

  const slotErr = slotError(date, time);
  if (slotErr) return json({ ok: false, error: slotErr }, 400);
  if (name.length < 2) return json({ ok: false, error: 'bad_name' }, 400);
  if (business.length < 2) return json({ ok: false, error: 'bad_business' }, 400);
  if (phone.replace(/\D/g, '').length < 7) return json({ ok: false, error: 'bad_phone' }, 400);
  if (email && !EMAIL_RE.test(email)) return json({ ok: false, error: 'bad_email' }, 400);

  const a = body.attribution && typeof body.attribution === 'object' ? body.attribution : {};
  const b = {
    id: randomId('bk_'),
    date, time, name, phone, business,
    email: email || null,
    note: note || null,
    source: cleanOrNull(body.source, 40),
    utm_source: cleanOrNull(a.utm_source, 100),
    utm_medium: cleanOrNull(a.utm_medium, 100),
    utm_campaign: cleanOrNull(a.utm_campaign, 150),
    utm_content: cleanOrNull(a.utm_content, 150),
    utm_term: cleanOrNull(a.utm_term, 150),
    fbclid: cleanOrNull(a.fbclid, 500),
    landing: cleanOrNull(a.landing, 300),
    referrer: cleanOrNull(a.referrer, 300),
    created_at: new Date().toISOString(),
    ip_hash: ipH
  };

  try {
    await env.DB.prepare(
      'INSERT INTO bookings (id, date, time, name, phone, business, email, note, source, ' +
      'utm_source, utm_medium, utm_campaign, utm_content, utm_term, fbclid, landing, referrer, ' +
      "status, created_at, ip_hash) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15, ?16, ?17, 'booked', ?18, ?19)"
    ).bind(
      b.id, b.date, b.time, b.name, b.phone, b.business, b.email, b.note, b.source,
      b.utm_source, b.utm_medium, b.utm_campaign, b.utm_content, b.utm_term, b.fbclid, b.landing, b.referrer,
      b.created_at, b.ip_hash
    ).run();
  } catch (err) {
    if (/UNIQUE constraint failed/i.test(String(err && err.message))) {
      return json({ ok: false, error: 'slot_taken' }, 409);
    }
    throw err;
  }

  // Meta needs a click id cookie value; rebuild one from fbclid if the
  // browser didn't have _fbc yet.
  let fbc = clean(a.fbc, 500);
  if (!fbc && b.fbclid) fbc = 'fb.1.' + Date.now() + '.' + b.fbclid;
  const site = env.SITE_URL || 'https://nuevoautomations.com';
  const referer = request.headers.get('referer') || '';
  runSideEffects(env, ctx, b, {
    consent: body.consent === true,
    event_id: clean(body.event_id, 64) || b.id,
    ip,
    ua: request.headers.get('user-agent') || '',
    fbc: fbc || null,
    fbp: clean(a.fbp, 200) || null,
    page_url: hostOf(referer) === hostOf(site) ? referer.slice(0, 300) : site + '/book/'
  });

  return json({ ok: true, id: b.id, date: b.date, time: b.time });
}

// POST /api/track  (anonymous, cookieless analytics)
const TRACK_TYPES = new Set(['pageview', 'cta', 'book_view', 'book_start']);

export async function track(request, env) {
  if (!originAllowed(request)) return noContent();
  let body;
  try { body = await readJson(request, 2048); } catch (e) { return noContent(); }

  const type = clean(body.type, 20);
  if (!TRACK_TYPES.has(type)) return json({ ok: false, error: 'bad_type' }, 400);

  const ua = request.headers.get('user-agent') || '';
  // Skip obvious bots so they don't inflate visitor counts.
  if (/bot|crawl|spider|slurp|headless|lighthouse|preview|facebookexternalhit/i.test(ua)) return noContent();

  const visitor = await visitorHash(env, clientIp(request), ua);
  if (!(await rateLimit(env, 'track:' + visitor, 120))) return noContent();

  let path = clean(body.path, 200);
  if (path && path[0] !== '/') path = '/' + path;
  const self = hostOf(request.url);
  let refHost = hostOf(clean(body.ref, 500));
  if (refHost === self) refHost = null; // internal navigation isn't a source

  await env.DB.prepare(
    'INSERT INTO events (ts, type, path, ref_host, utm_source, utm_campaign, visitor) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)'
  ).bind(
    new Date().toISOString(), type, path || null, refHost ? refHost.slice(0, 100) : null,
    cleanOrNull(body.utm_source, 100), cleanOrNull(body.utm_campaign, 150), visitor
  ).run();
  return noContent();
}

// GET /api/calendar.ics?key=CALENDAR_KEY — private feed for Google Calendar.
export async function calendarFeed(request, env) {
  const key = new URL(request.url).searchParams.get('key') || '';
  if (!env.CALENDAR_KEY || !(await safeEqual(key, env.CALENDAR_KEY))) {
    return json({ ok: false, error: 'not_found' }, 404);
  }
  const { results } = await env.DB.prepare(
    "SELECT * FROM bookings WHERE status = 'booked' AND date >= ?1 ORDER BY date, time LIMIT 2000"
  ).bind(addDays(dubaiToday(), -30)).all();
  const body = calendar('Nuevo bookings', results.map(internalEvent));
  return new Response(body, {
    headers: {
      'Content-Type': 'text/calendar; charset=utf-8',
      'Content-Disposition': 'inline; filename="nuevo-bookings.ics"',
      'Cache-Control': 'private, no-store',
      'X-Robots-Tag': 'noindex'
    }
  });
}
