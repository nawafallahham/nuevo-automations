// Shared helpers: responses, hashing, Dubai clock, slot rules, rate limiting.

// ---- Booking window (must match js/booking.js) ------------------------
export const OPEN_MIN = 14 * 60;        // first slot 14:00 Dubai
export const CLOSE_MIN = 18 * 60 + 30;  // last slot 18:30 Dubai
export const STEP_MIN = 30;
export const LEAD_MIN = 45;             // no slot less than 45 min away
export const MAX_DAYS_AHEAD = 14;
export const DUBAI_OFFSET_MS = 4 * 60 * 60 * 1000; // GST, UTC+4, no DST
export const MEETING_MIN = 20;

// ---- Responses ----------------------------------------------------------
const BASE_HEADERS = {
  'Content-Type': 'application/json; charset=utf-8',
  'Cache-Control': 'no-store',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin'
};

export function json(body, status = 200, extra = {}) {
  return new Response(JSON.stringify(body), { status, headers: { ...BASE_HEADERS, ...extra } });
}

export function noContent() {
  return new Response(null, { status: 204, headers: { 'Cache-Control': 'no-store' } });
}

// Read a JSON body with a size cap. sendBeacon posts text/plain, so we
// parse the text ourselves rather than trusting Content-Type.
export async function readJson(request, maxBytes = 8192) {
  const len = Number(request.headers.get('content-length') || 0);
  if (len > maxBytes) throw new HttpError(413, 'too_large');
  const text = await request.text();
  if (text.length > maxBytes) throw new HttpError(413, 'too_large');
  if (!text) return {};
  try {
    const v = JSON.parse(text);
    return v && typeof v === 'object' && !Array.isArray(v) ? v : {};
  } catch (e) {
    throw new HttpError(400, 'bad_json');
  }
}

export class HttpError extends Error {
  constructor(status, code) { super(code); this.status = status; this.code = code; }
}

// ---- Strings ------------------------------------------------------------
// Strip control characters, trim, cap length.
export function clean(s, max) {
  const str = String(s == null ? '' : s);
  let out = '';
  for (let i = 0; i < str.length; i++) {
    const c = str.charCodeAt(i);
    if (c >= 32 && c !== 127) out += str.charAt(i);
  }
  return out.trim().slice(0, max);
}

export function cleanOrNull(s, max) {
  const v = clean(s, max);
  return v ? v : null;
}

export function escapeHtml(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

export function hostOf(url) {
  try { return new URL(url).hostname.replace(/^www\./, '').toLowerCase(); } catch (e) { return null; }
}

// Digits-only phone with UAE country code assumed for local formats.
export function normalisePhone(phone) {
  let d = String(phone || '').replace(/\D/g, '');
  if (d.startsWith('00')) d = d.slice(2);
  if (d.length === 10 && d.startsWith('05')) d = '971' + d.slice(1);  // 050 123 4567
  else if (d.length === 9 && d.startsWith('5')) d = '971' + d;        // 50 123 4567
  return d;
}

export function waLink(phone, text) {
  const d = normalisePhone(phone);
  return 'https://wa.me/' + d + (text ? '?text=' + encodeURIComponent(text) : '');
}

// ---- Crypto -------------------------------------------------------------
const enc = new TextEncoder();

export async function sha256Hex(s) {
  const buf = await crypto.subtle.digest('SHA-256', enc.encode(String(s)));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

// Constant-time comparison: hash both sides so lengths match, then compare
// every byte without early exit.
export async function safeEqual(a, b) {
  if (!a || !b) return false;
  const [x, y] = await Promise.all([
    crypto.subtle.digest('SHA-256', enc.encode(String(a))),
    crypto.subtle.digest('SHA-256', enc.encode(String(b)))
  ]);
  const ua = new Uint8Array(x), ub = new Uint8Array(y);
  let diff = 0;
  for (let i = 0; i < ua.length; i++) diff |= ua[i] ^ ub[i];
  return diff === 0;
}

export function randomId(prefix, bytes = 9) {
  const a = new Uint8Array(bytes);
  crypto.getRandomValues(a);
  return prefix + [...a].map((b) => b.toString(16).padStart(2, '0')).join('');
}

export function clientIp(request) {
  return request.headers.get('cf-connecting-ip') ||
    (request.headers.get('x-forwarded-for') || '').split(',')[0].trim() || '0.0.0.0';
}

function salt(env) { return env.HASH_SALT || 'nuevo-site-v1'; }

// Stable per-IP hash for bookings / rate limits (never the raw IP).
export async function ipHash(env, ip) {
  return (await sha256Hex('ip|' + salt(env) + '|' + ip)).slice(0, 24);
}

// Anonymous analytics visitor id. The salt rotates every Dubai day, so a
// visitor can't be followed from one day to the next or reversed to an IP.
export async function visitorHash(env, ip, ua) {
  const day = dubaiToday();
  return (await sha256Hex('v|' + salt(env) + '|' + day + '|' + ip + '|' + ua)).slice(0, 20);
}

// ---- Dubai clock ----------------------------------------------------------
export function dubaiNow(now = Date.now()) {
  return new Date(now + DUBAI_OFFSET_MS); // read with getUTC* for Dubai wall time
}

export function dubaiToday(now = Date.now()) {
  return dubaiNow(now).toISOString().slice(0, 10);
}

export function addDays(isoDate, n) {
  const d = new Date(isoDate + 'T00:00:00Z');
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
}

// UTC instant for a Dubai date + HH:MM.
export function slotInstant(date, time) {
  return new Date(Date.parse(date + 'T' + time + ':00Z') - DUBAI_OFFSET_MS);
}

export function isValidTimeFormat(t) {
  if (!/^\d{2}:\d{2}$/.test(t || '')) return false;
  const mins = Number(t.slice(0, 2)) * 60 + Number(t.slice(3, 5));
  if (mins < OPEN_MIN || mins > CLOSE_MIN) return false;
  return (mins - OPEN_MIN) % STEP_MIN === 0;
}

// Returns null if the slot is bookable, otherwise an error code.
export function slotError(date, time, now = Date.now()) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date || '') || isNaN(Date.parse(date + 'T00:00:00Z'))) return 'bad_date';
  if (!isValidTimeFormat(time)) return 'bad_time';
  const today = dubaiToday(now);
  if (date < today || date > addDays(today, MAX_DAYS_AHEAD)) return 'bad_date';
  if (slotInstant(date, time).getTime() < now + LEAD_MIN * 60 * 1000) return 'too_soon';
  return null;
}

// ---- Rate limiting (fixed hourly window in D1) ---------------------------
export function hourWindow(now = Date.now()) {
  return new Date(now).toISOString().slice(0, 13); // 'YYYY-MM-DDTHH'
}

// Increments the counter and returns true if the caller is still under limit.
export async function rateLimit(env, key, limit) {
  const win = hourWindow();
  const row = await env.DB.prepare(
    'INSERT INTO rate (key, count, "window") VALUES (?1, 1, ?2) ' +
    'ON CONFLICT(key) DO UPDATE SET ' +
    'count = CASE WHEN rate."window" = excluded."window" THEN rate.count + 1 ELSE 1 END, ' +
    '"window" = excluded."window" RETURNING count'
  ).bind(key, win).first();
  return !row || row.count <= limit;
}

// Same-origin guard for state-changing requests. Browsers always send
// Origin on POST; if present it must be this same host.
export function originAllowed(request) {
  const origin = request.headers.get('origin');
  if (!origin) return true;
  const h = hostOf(origin);
  const self = new URL(request.url).hostname.replace(/^www\./, '');
  return h === self;
}
