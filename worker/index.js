// nuevoautomations.com — one Worker for the static site and the /api backend.
//
//   /api/slots            GET   taken slots (public)
//   /api/book             POST  create a booking (public)
//   /api/track            POST  anonymous analytics beacon (public)
//   /api/calendar.ics     GET   private iCal feed (?key=CALENDAR_KEY)
//   /api/calendly/webhook POST  Calendly invitee.created / invitee.canceled (signed)
//   /api/calendly/scheduled POST browser beacon after a Calendly booking (public)
//   /api/lead             POST  qualifying-question progress (public)
//   /api/admin/*          *     dashboard API (Bearer ADMIN_KEY)
//   everything else             static files from env.ASSETS
import { json, HttpError, hourWindow, addDays, dubaiToday } from './lib.js';
import { slots, book, track, calendarFeed } from './api.js';
import { admin } from './admin.js';
import { lead } from './leads.js';
import { webhook as calendlyWebhook, scheduledBeacon as calendlyScheduled } from './calendly.js';

const APEX = 'nuevoautomations.com';

async function route(request, env, ctx) {
  const url = new URL(request.url);
  const path = url.pathname.replace(/\/+$/, '') || '/';
  const m = request.method;

  if (m === 'OPTIONS') return new Response(null, { status: 204, headers: { Allow: 'GET, POST, OPTIONS' } });

  if (path === '/api/slots' && m === 'GET') return slots(request, env);
  if (path === '/api/book' && m === 'POST') return book(request, env, ctx);
  if (path === '/api/track' && m === 'POST') return track(request, env);
  if (path === '/api/calendar.ics' && m === 'GET') return calendarFeed(request, env);
  if (path === '/api/calendly/webhook' && m === 'POST') return calendlyWebhook(request, env, ctx);
  if (path === '/api/calendly/scheduled' && m === 'POST') return calendlyScheduled(request, env, ctx);
  if (path === '/api/lead' && m === 'POST') return lead(request, env, ctx);
  if (path.startsWith('/api/admin/')) return admin(request, env, path);

  return json({ ok: false, error: 'not_found' }, 404);
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // www -> apex and http -> https, keeping path and query.
    if (url.hostname === 'www.' + APEX || (url.hostname === APEX && url.protocol === 'http:')) {
      return Response.redirect('https://' + APEX + url.pathname + url.search, 301);
    }

    if (url.pathname === '/api' || url.pathname.startsWith('/api/')) {
      try {
        return await route(request, env, ctx);
      } catch (err) {
        if (err instanceof HttpError) return json({ ok: false, error: err.code }, err.status);
        console.error('[api] ' + request.method + ' ' + url.pathname + ': ' + (err && err.stack || err));
        return json({ ok: false, error: 'server_error' }, 500);
      }
    }

    // The asset layer normalises trailing slashes (/m2s -> /m2s/, /index.html
    // -> /) with temporary redirects; make them permanent so link equity
    // consolidates on the canonical URL.
    const res = await env.ASSETS.fetch(request);
    if (res.status === 307 || res.status === 308) {
      const loc = res.headers.get('Location');
      if (loc) return Response.redirect(new URL(loc, url).toString(), 301);
    }
    // The *.workers.dev copy is for previews only; keep it out of search.
    if (url.hostname.endsWith('.workers.dev')) {
      const out = new Response(res.body, res);
      out.headers.set('X-Robots-Tag', 'noindex, nofollow');
      return out;
    }
    return res;
  },

  // Nightly retention clean-up (see privacy policy):
  //  - bookings deleted ~90 days after the appointment date
  //  - analytics events older than ~13 months
  //  - stale rate-limit rows
  //  - Calendly beacon rows (consent / attribution) after 2 days
  //  - qualifying-question leads after 180 days
  async scheduled(event, env, ctx) {
    const today = dubaiToday();
    const eventsCutoff = new Date(Date.now() - 400 * 24 * 3600 * 1000).toISOString();
    const rateCutoff = hourWindow(Date.now() - 2 * 3600 * 1000);
    ctx.waitUntil(env.DB.batch([
      env.DB.prepare('DELETE FROM bookings WHERE date < ?1').bind(addDays(today, -90)),
      env.DB.prepare('DELETE FROM events WHERE ts < ?1').bind(eventsCutoff),
      env.DB.prepare('DELETE FROM rate WHERE "window" < ?1').bind(rateCutoff),
      env.DB.prepare('DELETE FROM calendly_pending WHERE created_at < ?1')
        .bind(new Date(Date.now() - 2 * 24 * 3600 * 1000).toISOString()),
      env.DB.prepare('DELETE FROM leads WHERE created_at < ?1')
        .bind(new Date(Date.now() - 180 * 24 * 3600 * 1000).toISOString())
    ]).catch((err) => console.error('[cron] ' + err.message)));
  }
};
