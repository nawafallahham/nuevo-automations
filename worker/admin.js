// /api/admin/* — private dashboard API. Bearer ADMIN_KEY on every request.
import { json, readJson, safeEqual, dubaiToday, addDays, slotInstant, hostOf } from './lib.js';
import { calendlySetup, calendlyStatus } from './calendly.js';
import { sendMetaWon } from './notify.js';

export async function admin(request, env, path, ctx) {
  if (!env.ADMIN_KEY) return json({ ok: false, error: 'admin_key_not_set' }, 503);
  const auth = request.headers.get('authorization') || '';
  const given = auth.startsWith('Bearer ') ? auth.slice(7).trim() : '';
  if (!(await safeEqual(given, env.ADMIN_KEY))) {
    return json({ ok: false, error: 'unauthorised' }, 401, { 'WWW-Authenticate': 'Bearer' });
  }

  const m = request.method;
  if (m === 'GET' && path === '/api/admin/bookings') return bookings(request, env);
  if (m === 'GET' && path === '/api/admin/stats') return stats(request, env);
  if (m === 'GET' && path === '/api/admin/leads') return leads(request, env);
  if (m === 'GET' && path === '/api/admin/config') return config(env);
  if (m === 'GET' && path === '/api/admin/calendly/status') return calendlyStatus(env);
  if (m === 'POST' && path === '/api/admin/calendly/setup') return calendlySetup(env);
  const cancel = path.match(/^\/api\/admin\/bookings\/(bk_[a-f0-9]{6,40})\/cancel$/);
  if (m === 'POST' && cancel) return cancelBooking(env, cancel[1]);
  const won = path.match(/^\/api\/admin\/leads\/(ld_[a-f0-9]{16,40})\/won$/);
  if (m === 'POST' && won) return markWon(request, env, ctx, won[1]);
  return json({ ok: false, error: 'not_found' }, 404);
}

async function bookings(request, env) {
  const scope = new URL(request.url).searchParams.get('scope') === 'all' ? 'all' : 'upcoming';
  const sql = scope === 'all'
    ? 'SELECT * FROM bookings ORDER BY date DESC, time DESC LIMIT 500'
    : "SELECT * FROM bookings WHERE status = 'booked' AND date >= ?1 ORDER BY date, time LIMIT 500";
  const stmt = env.DB.prepare(sql);
  const { results } = await (scope === 'all' ? stmt : stmt.bind(dubaiToday())).all();
  results.forEach((r) => { delete r.ip_hash; });
  return json({ ok: true, scope, count: results.length, bookings: results });
}

async function cancelBooking(env, id) {
  const r = await env.DB.prepare(
    "UPDATE bookings SET status = 'cancelled' WHERE id = ?1 AND status = 'booked'"
  ).bind(id).run();
  const changed = (r.meta && r.meta.changes) || 0;
  if (!changed) return json({ ok: false, error: 'not_found_or_already_cancelled' }, 404);
  return json({ ok: true, id, status: 'cancelled' });
}

// POST /api/admin/leads/:id/won {value} — the lead signed. Sends Meta a
// Purchase once, and only for leads whose Lead event went out (they
// accepted cookies), so Meta can optimise for clients, not just calls.
async function markWon(request, env, ctx, id) {
  const body = await readJson(request, 1024);
  const value = Math.round(Number(body.value) * 100) / 100;
  if (!(value > 0 && value < 10000000)) return json({ ok: false, error: 'bad_value' }, 400);
  const now = new Date().toISOString();
  const r = await env.DB.prepare(
    'UPDATE leads SET won_at = COALESCE(won_at, ?2), won_value = ?3 WHERE id = ?1'
  ).bind(id, now, value).run();
  if (!((r.meta && r.meta.changes) || 0)) return json({ ok: false, error: 'not_found' }, 404);

  let meta = 'skipped: no consent or no number';
  const l = await env.DB.prepare(
    'SELECT l.id, l.name, l.capi_lead_at, COALESCE(l.phone, b.phone) AS phone FROM leads l ' +
    'LEFT JOIN bookings b ON b.calendly_invitee_uri = l.invitee_uri WHERE l.id = ?1'
  ).bind(id).first();
  if (!env.META_CAPI_TOKEN || !env.META_PIXEL_ID) meta = 'skipped: META_CAPI_TOKEN not set';
  else if (l && l.phone && l.capi_lead_at) {
    const claim = await env.DB.prepare('UPDATE leads SET capi_won_at = ?2 WHERE id = ?1 AND capi_won_at IS NULL')
      .bind(id, now).run();
    if (claim.meta && claim.meta.changes === 1) {
      meta = 'sent';
      ctx.waitUntil(sendMetaWon(env, l, value)
        .catch((err) => console.error('[meta_Purchase] ' + id + ': ' + (err && err.message || err))));
    } else meta = 'already sent';
  }
  return json({ ok: true, id, won_value: value, meta });
}

function config(env) {
  const site = env.SITE_URL || 'https://nuevoautomations.com';
  return json({
    ok: true,
    calendar_url: env.CALENDAR_KEY ? site + '/api/calendar.ics?key=' + encodeURIComponent(env.CALENDAR_KEY) : null,
    integrations: {
      meta_capi: Boolean(env.META_CAPI_TOKEN && env.META_PIXEL_ID),
      meta_test_mode: Boolean(env.META_TEST_EVENT_CODE),
      email: Boolean(env.EMAIL || env.RESEND_API_KEY),
      notify_email: env.NOTIFY_EMAIL || 'nawafallahham@nuevoautomations.com',
      orcaflo: Boolean(env.ORCAFLO_HOOK_URL && env.ORCAFLO_HOOK_SECRET),
      calendar_feed: Boolean(env.CALENDAR_KEY),
      calendly: Boolean(env.CALENDLY_TOKEN && env.CALENDLY_SIGNING_KEY)
    }
  });
}

function rate(n, d) { return d ? Math.round((n / d) * 10000) / 100 : 0; } // percent, 2dp

function bookingSource(b) {
  const ref = hostOf(b.referrer);
  return b.utm_source || (ref && ref !== 'nuevoautomations.com' ? ref : null) || 'direct';
}

// Which channel a visit or lead came from. Events only keep utm_source,
// utm_campaign and the referring host, so medium is optional here.
const CHANNELS = ['Google Ads', 'Google Business Profile', 'Google search', 'Meta ads', 'Facebook / Instagram (organic)', 'Other', 'Direct'];
function channelOf(src, medium, campaign, refHost) {
  const s = (src || '').toLowerCase();
  const m = (medium || '').toLowerCase();
  const r = (refHost || '').toLowerCase();
  if (s === 'google') {
    if ((campaign || '').toLowerCase() === 'gbp') return 'Google Business Profile';
    return m === 'organic' ? 'Google search' : 'Google Ads';
  }
  if (/^(facebook|fb|instagram|ig|meta|an|msg)$/.test(s)) return 'Meta ads';
  if (s) return 'Other';
  if (/(^|\.)google\./.test(r)) return 'Google search';
  if (/(^|\.)(facebook|instagram)\.com$|^(l|lm|m)\.facebook\.com$/.test(r)) return 'Facebook / Instagram (organic)';
  if (r) return 'Other';
  return 'Direct';
}

async function stats(request, env) {
  const days = Math.min(Math.max(parseInt(new URL(request.url).searchParams.get('days'), 10) || 30, 1), 365);
  const today = dubaiToday();
  const firstDay = addDays(today, -(days - 1));
  const since = slotInstant(firstDay, '00:00').toISOString(); // start of that Dubai day, in UTC
  const DUBAI_DAY = "substr(datetime(ts, '+4 hours'), 1, 10)";

  const [totals, perVisitor, byDayEv, topPages, bks] = await env.DB.batch([
    env.DB.prepare(
      "SELECT SUM(type = 'pageview') AS pageviews, COUNT(DISTINCT CASE WHEN type = 'pageview' THEN visitor END) AS visitors, " +
      "SUM(type = 'book_view') AS book_page_views, SUM(type = 'book_start') AS book_starts, SUM(type = 'cta') AS cta_clicks " +
      'FROM events WHERE ts >= ?1'
    ).bind(since),
    env.DB.prepare(
      "SELECT visitor, MAX(utm_source) AS us, MAX(utm_campaign) AS uc, MAX(ref_host) AS rh FROM events " +
      "WHERE ts >= ?1 AND type = 'pageview' GROUP BY visitor"
    ).bind(since),
    env.DB.prepare(
      'SELECT ' + DUBAI_DAY + " AS day, SUM(type = 'pageview') AS pageviews, " +
      "COUNT(DISTINCT CASE WHEN type = 'pageview' THEN visitor END) AS visitors, SUM(type = 'book_view') AS book_views " +
      'FROM events WHERE ts >= ?1 GROUP BY day ORDER BY day'
    ).bind(since),
    env.DB.prepare(
      "SELECT path, COUNT(*) AS views, COUNT(DISTINCT visitor) AS visitors FROM events " +
      "WHERE ts >= ?1 AND type = 'pageview' GROUP BY path ORDER BY views DESC LIMIT 15"
    ).bind(since),
    env.DB.prepare(
      'SELECT id, created_at, status, source, utm_source, utm_campaign, referrer FROM bookings WHERE created_at >= ?1'
    ).bind(since)
  ]);

  const t = (totals.results && totals.results[0]) || {};
  const bookingRows = bks.results || [];
  const bookingsMade = bookingRows.length;
  const cancelled = bookingRows.filter((b) => b.status === 'cancelled').length;

  // Traffic & bookings per source/campaign.
  const groups = new Map();
  const bucket = (source, campaign) => {
    const k = source + '\u0000' + campaign;
    if (!groups.has(k)) groups.set(k, { source, campaign, visitors: 0, bookings: 0 });
    return groups.get(k);
  };
  for (const v of perVisitor.results || []) bucket(v.us || v.rh || 'direct', v.uc || '').visitors++;
  for (const b of bookingRows) bucket(bookingSource(b), b.utm_campaign || '').bookings++;
  const bySource = [...groups.values()]
    .map((g) => ({ ...g, conversion: rate(g.bookings, g.visitors) }))
    .sort((a, b) => b.bookings - a.bookings || b.visitors - a.visitors)
    .slice(0, 50);

  // Daily series with every day present (zeros included).
  const evByDay = new Map((byDayEv.results || []).map((r) => [r.day, r]));
  const bkByDay = new Map();
  for (const b of bookingRows) {
    const d = new Date(Date.parse(b.created_at) + 4 * 3600 * 1000).toISOString().slice(0, 10);
    bkByDay.set(d, (bkByDay.get(d) || 0) + 1);
  }
  const byDay = [];
  for (let i = 0; i < days; i++) {
    const d = addDays(firstDay, i);
    const e = evByDay.get(d) || {};
    byDay.push({ day: d, visitors: e.visitors || 0, pageviews: e.pageviews || 0, book_views: e.book_views || 0, bookings: bkByDay.get(d) || 0 });
  }

  const visitors = t.visitors || 0;
  const bookViews = t.book_page_views || 0;
  return json({
    ok: true,
    days,
    since,
    pageviews: t.pageviews || 0,
    visitors,
    book_page_views: bookViews,
    book_starts: t.book_starts || 0,
    cta_clicks: t.cta_clicks || 0,
    bookings: bookingsMade,
    cancelled,
    conversion: {
      visitor_to_booking: rate(bookingsMade, visitors),
      visitor_to_book_view: rate(bookViews, visitors),
      book_view_to_booking: rate(bookingsMade, bookViews)
    },
    by_source: bySource,
    by_day: byDay,
    top_pages: topPages.results || [],
    note: 'Visitors are counted per day (the anonymous id rotates daily), so multi-day totals count a returning visitor once per day.'
  });
}

// GET /api/admin/leads?days=30 — the qualifying-question funnel and every lead.
async function leads(request, env) {
  const days = Math.min(Math.max(parseInt(new URL(request.url).searchParams.get('days'), 10) || 30, 1), 365);
  const since = slotInstant(addDays(dubaiToday(), -(days - 1)), '00:00').toISOString();

  const [ev, perVisitor, rows] = await env.DB.batch([
    env.DB.prepare(
      "SELECT COUNT(DISTINCT CASE WHEN type = 'pageview' THEN visitor END) AS visitors, " +
      "COUNT(DISTINCT CASE WHEN type = 'book_view' THEN visitor END) AS book_viewers FROM events WHERE ts >= ?1"
    ).bind(since),
    env.DB.prepare(
      "SELECT MAX(utm_source) AS us, MAX(utm_campaign) AS uc, MAX(ref_host) AS rh FROM events " +
      "WHERE ts >= ?1 AND type = 'pageview' GROUP BY visitor"
    ).bind(since),
    env.DB.prepare(
      'SELECT l.id, l.created_at, l.updated_at, l.page, l.status, l.step, l.q1, l.q2, l.q3, l.q4, l.declined_at_q, ' +
      'l.name, l.company, l.booked_at, l.won_at, l.won_value, l.utm_source, l.utm_medium, l.utm_campaign, l.utm_content, l.landing, l.referrer, ' +
      'b.date AS booking_date, b.time AS booking_time, b.status AS booking_status, b.email AS email, COALESCE(l.phone, b.phone) AS phone ' +
      'FROM leads l LEFT JOIN bookings b ON b.calendly_invitee_uri = l.invitee_uri ' +
      'WHERE l.created_at >= ?1 ORDER BY l.created_at DESC LIMIT 2000'
    ).bind(since)
  ]);
  const e = (ev.results && ev.results[0]) || {};
  const list = rows.results || [];
  const count = (f) => list.filter(f).length;
  const passed = (l) => l.status === 'qualified' || l.status === 'details' || l.status === 'booked';

  const funnel = [
    ['Visitors', e.visitors || 0],
    ['Saw the booking section', e.book_viewers || 0],
    ['Started (gave details or answered)', list.length],
    ['Gave name and WhatsApp number', count((l) => !!l.phone)],
    ['Answered question 1', count((l) => l.step >= 1)],
    ['Answered question 2', count((l) => l.step >= 2)],
    ['Answered question 3', count((l) => l.step >= 3)],
    ['Answered question 4', count((l) => l.step >= 4)],
    ['Qualified', count(passed)],
    ['Gave company name', count((l) => l.status === 'details' || l.status === 'booked')],
    ['Booked a call', count((l) => l.status === 'booked')],
    ['Booking still on (not cancelled)', count((l) => l.status === 'booked' && l.booking_status !== 'cancelled')]
  ].map(([label, n]) => ({ label, n }));

  // Answer counts per question, with how many of each went on to book.
  const questions = ['q1', 'q2', 'q3', 'q4'].map((q, i) => {
    const m = new Map();
    for (const l of list) {
      if (!l[q]) continue;
      const r = m.get(l[q]) || { answer: l[q], n: 0, declined: 0, booked: 0 };
      r.n++;
      if (l.declined_at_q === i + 1) r.declined++;
      if (l.status === 'booked') r.booked++;
      m.set(l[q], r);
    }
    return [...m.values()].sort((a, b) => b.n - a.n);
  });

  const group = (keyOf) => {
    const m = new Map();
    for (const l of list) {
      const k = keyOf(l);
      const r = m.get(k) || { key: k, started: 0, declined: 0, qualified: 0, details: 0, booked: 0 };
      r.started++;
      if (l.status === 'declined') r.declined++;
      if (passed(l)) r.qualified++;
      if (l.status === 'details' || l.status === 'booked') r.details++;
      if (l.status === 'booked') r.booked++;
      m.set(k, r);
    }
    return [...m.values()].sort((a, b) => b.started - a.started);
  };

  // Google vs Meta: visitors through to won clients, per channel.
  const ch = new Map(CHANNELS.map((c) => [c, { key: c, visitors: 0, started: 0, contact: 0, qualified: 0, booked: 0, won: 0, won_value: 0 }]));
  for (const v of perVisitor.results || []) ch.get(channelOf(v.us, null, v.uc, v.rh)).visitors++;
  for (const l of list) {
    const r = ch.get(channelOf(l.utm_source, l.utm_medium, l.utm_campaign, hostOf(l.referrer)));
    r.started++;
    if (l.phone) r.contact++;
    if (passed(l)) r.qualified++;
    if (l.status === 'booked') r.booked++;
    if (l.won_at) { r.won++; r.won_value += Number(l.won_value) || 0; }
  }
  const byChannel = [...ch.values()].filter((r) => r.visitors || r.started);

  return json({
    ok: true,
    days,
    funnel,
    by_channel: byChannel,
    questions,
    by_page: group((l) => l.page || 'unknown'),
    by_source: group((l) => [l.utm_source || hostOf(l.referrer) || 'direct', l.utm_campaign].filter(Boolean).join(' / ')),
    leads: list
  });
}
