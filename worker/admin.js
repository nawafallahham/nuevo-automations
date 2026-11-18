// /api/admin/* — private dashboard API. Bearer ADMIN_KEY on every request.
import { json, safeEqual, dubaiToday, addDays, slotInstant, hostOf } from './lib.js';

export async function admin(request, env, path) {
  if (!env.ADMIN_KEY) return json({ ok: false, error: 'admin_key_not_set' }, 503);
  const auth = request.headers.get('authorization') || '';
  const given = auth.startsWith('Bearer ') ? auth.slice(7).trim() : '';
  if (!(await safeEqual(given, env.ADMIN_KEY))) {
    return json({ ok: false, error: 'unauthorised' }, 401, { 'WWW-Authenticate': 'Bearer' });
  }

  const m = request.method;
  if (m === 'GET' && path === '/api/admin/bookings') return bookings(request, env);
  if (m === 'GET' && path === '/api/admin/stats') return stats(request, env);
  if (m === 'GET' && path === '/api/admin/config') return config(env);
  const cancel = path.match(/^\/api\/admin\/bookings\/(bk_[a-f0-9]{6,40})\/cancel$/);
  if (m === 'POST' && cancel) return cancelBooking(env, cancel[1]);
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

function config(env) {
  const site = env.SITE_URL || 'https://nuevoautomations.com';
  return json({
    ok: true,
    calendar_url: env.CALENDAR_KEY ? site + '/api/calendar.ics?key=' + encodeURIComponent(env.CALENDAR_KEY) : null,
    integrations: {
      meta_capi: Boolean(env.META_CAPI_TOKEN && env.META_PIXEL_ID),
      meta_test_mode: Boolean(env.META_TEST_EVENT_CODE),
      email: Boolean(env.RESEND_API_KEY),
      notify_email: env.NOTIFY_EMAIL || 'nawafallahham@nuevoautomations.com',
      orcaflo: Boolean(env.ORCAFLO_HOOK_URL && env.ORCAFLO_HOOK_SECRET),
      calendar_feed: Boolean(env.CALENDAR_KEY)
    }
  });
}

function rate(n, d) { return d ? Math.round((n / d) * 10000) / 100 : 0; } // percent, 2dp

function bookingSource(b) {
  const ref = hostOf(b.referrer);
  return b.utm_source || (ref && ref !== 'nuevoautomations.com' ? ref : null) || 'direct';
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
