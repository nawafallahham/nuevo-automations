// Post-booking side effects. Each one is optional (skipped when its env vars
// are missing), runs inside ctx.waitUntil, and never throws back into the
// booking request — failures are only logged.
import { sha256Hex, normalisePhone, waLink, escapeHtml, slotInstant } from './lib.js';
import { calendar, internalEvent, customerEvent } from './ics.js';

export function runSideEffects(env, ctx, b, meta) {
  const jobs = [
    ['meta_capi', () => sendMetaCapi(env, b, meta)],
    ['email', () => sendEmails(env, b)],
    ['orcaflo', () => sendOrcaflo(env, b)]
  ];
  for (const [name, fn] of jobs) {
    ctx.waitUntil(
      Promise.resolve()
        .then(fn)
        .catch((err) => console.error('[' + name + '] ' + b.id + ': ' + (err && err.message || err)))
    );
  }
}

// ---- 1. Meta Conversions API ------------------------------------------------
// Also called directly by worker/calendly.js once both the webhook and the
// browser beacon have arrived (that's when consent is known).
export async function sendMetaCapi(env, b, meta) {
  if (!env.META_CAPI_TOKEN || !env.META_PIXEL_ID || meta.consent !== true) return;

  const firstName = (b.name || '').trim().split(/\s+/)[0].toLowerCase();
  const user = {
    client_ip_address: meta.ip,
    client_user_agent: meta.ua,
    country: [await sha256Hex('ae')]
  };
  if (b.phone) user.ph = [await sha256Hex(normalisePhone(b.phone))];
  if (firstName) user.fn = [await sha256Hex(firstName)];
  if (b.email) user.em = [await sha256Hex(b.email.trim().toLowerCase())];
  if (meta.fbc) user.fbc = meta.fbc;
  if (meta.fbp) user.fbp = meta.fbp;

  const body = {
    data: [{
      event_name: 'Schedule',
      event_time: Math.floor(Date.now() / 1000),
      event_id: meta.event_id,
      action_source: 'website',
      event_source_url: meta.page_url,
      user_data: user,
      custom_data: { content_name: b.provider === 'calendly' ? 'calendly' : b.date + ' ' + b.time }
    }]
  };
  await postCapi(env, body);
}

// The visitor gave their name and WhatsApp number before the qualifying
// questions (worker/leads.js). Same matching data as the Schedule event.
export async function sendMetaLead(env, l) {
  const firstName = (l.name || '').trim().split(/\s+/)[0].toLowerCase();
  const user = {
    client_ip_address: l.ip,
    client_user_agent: l.ua,
    country: [await sha256Hex('ae')],
    ph: [await sha256Hex(normalisePhone(l.phone))]
  };
  if (firstName) user.fn = [await sha256Hex(firstName)];
  if (l.fbc) user.fbc = l.fbc;
  if (l.fbp) user.fbp = l.fbp;
  await postCapi(env, {
    data: [{
      event_name: 'Lead',
      event_time: Math.floor(Date.now() / 1000),
      event_id: l.event_id,
      action_source: 'website',
      event_source_url: l.page_url,
      user_data: user,
      custom_data: { content_name: 'audit-contact' }
    }]
  });
}

async function postCapi(env, body) {
  if (env.META_TEST_EVENT_CODE) body.test_event_code = env.META_TEST_EVENT_CODE;
  const url = 'https://graph.facebook.com/v21.0/' + encodeURIComponent(env.META_PIXEL_ID) +
    '/events?access_token=' + encodeURIComponent(env.META_CAPI_TOKEN);
  const r = await fetchWithTimeout(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  }, 8000);
  if (!r.ok) throw new Error('CAPI ' + r.status + ': ' + (await r.text()).slice(0, 300));
}

// ---- 2. Email: Cloudflare Email Service (EMAIL binding) or Resend ------------
function b64(str) {
  const bytes = new TextEncoder().encode(str);
  let bin = '';
  for (let i = 0; i < bytes.length; i += 0x8000) {
    bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  }
  return btoa(bin);
}

function prettyWhen(b) {
  const d = new Date(b.date + 'T00:00:00Z');
  const day = new Intl.DateTimeFormat('en-GB', { timeZone: 'UTC', weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }).format(d);
  const h = Number(b.time.slice(0, 2)), m = b.time.slice(3);
  const t = (h % 12 === 0 ? 12 : h % 12) + ':' + m + ' ' + (h >= 12 ? 'PM' : 'AM');
  return day + ', ' + t + ' (Dubai time)';
}

async function resend(env, payload) {
  const r = await fetchWithTimeout('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + env.RESEND_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  }, 8000);
  if (!r.ok) throw new Error('Resend ' + r.status + ': ' + (await r.text()).slice(0, 300));
}

// One sender for both providers. Cloudflare's binding is preferred: no API key,
// and mail to the owner's verified address is free on every plan. Mailing
// customers (any address) through it needs Workers Paid, so that is opt-in via
// EMAIL_CUSTOMERS=true; with Resend it is always on.
async function sendMail(env, msg) {
  if (env.EMAIL) {
    await env.EMAIL.send({
      to: msg.to[0],
      from: msg.from,
      subject: msg.subject,
      text: msg.text,
      html: msg.html,
      replyTo: msg.reply_to,
      attachments: (msg.attachments || []).map((a) => ({
        content: a.content, filename: a.filename, type: 'text/calendar', disposition: 'attachment'
      }))
    });
    return;
  }
  await resend(env, msg);
}

async function sendEmails(env, b) {
  if (!env.EMAIL && !env.RESEND_API_KEY) return;
  // Calendly already emails the invitee a confirmation + invite.
  const viaCalendly = b.provider === 'calendly';
  const mailCustomers = !viaCalendly && (!env.EMAIL || env.EMAIL_CUSTOMERS === 'true');
  const from = env.MAIL_FROM || 'Nuevo Automations <bookings@nuevoautomations.com>';
  const to = env.NOTIFY_EMAIL || 'nawafallahham@nuevoautomations.com';
  const when = prettyWhen(b);
  const wa = b.phone && waLink(b.phone, 'Hi ' + b.name.split(/\s+/)[0] + ', this is Nawaf from Nuevo Automations about your M2S audit on ' + when + '.');

  const rows = [
    ['When', when],
    ['Name', b.name],
    ['Business', b.business || '—'],
    ['WhatsApp', b.phone || '—'],
    ['Email', b.email || '—'],
    ['Booked from', (b.source || '—') + (viaCalendly && b.source !== 'calendly' ? ' (via Calendly)' : '')],
    ['UTM source / medium', [b.utm_source, b.utm_medium].filter(Boolean).join(' / ') || '—'],
    ['UTM campaign', b.utm_campaign || '—'],
    ['UTM content / term', [b.utm_content, b.utm_term].filter(Boolean).join(' / ') || '—'],
    ['Landing page', b.landing || '—'],
    ['Referrer', b.referrer || '—'],
    ['fbclid', b.fbclid ? 'yes' : 'no'],
    ['Booking id', b.id]
  ];
  if (b.note) rows.splice(6, 0, ['Answers', b.note]);
  if (b.cancel_url) rows.push(['Cancel (Calendly)', b.cancel_url]);
  if (b.reschedule_url) rows.push(['Reschedule (Calendly)', b.reschedule_url]);

  const text = 'New M2S audit booked.\n\n' +
    rows.map((r) => r[0] + ': ' + r[1]).join('\n') +
    (wa ? '\n\nMessage on WhatsApp: ' + wa + '\n' : '\n');
  const html = '<div style="font-family:Inter,Arial,sans-serif;color:#101a2b;font-size:15px;line-height:1.5">' +
    '<h2 style="margin:0 0 12px;font-size:18px">New M2S audit booked</h2>' +
    '<table cellpadding="6" style="border-collapse:collapse">' +
    rows.map((r) => '<tr><td style="color:#4b5768;border-bottom:1px solid #e3e7ec">' + escapeHtml(r[0]) +
      '</td><td style="border-bottom:1px solid #e3e7ec"><strong>' + escapeHtml(r[1]) + '</strong></td></tr>').join('') +
    '</table>' + (wa ? '<p style="margin:18px 0"><a href="' + escapeHtml(wa) + '" style="background:#1fae56;color:#fff;padding:10px 16px;border-radius:8px;text-decoration:none;font-weight:600">Message ' +
    escapeHtml(b.name) + ' on WhatsApp</a></p>' : '') + '</div>';

  const internalIcs = calendar(null, [internalEvent(b)], 'PUBLISH');
  const jobs = [sendMail(env, {
    from,
    to: [to],
    subject: 'New M2S audit: ' + (b.business || b.name) + ' — ' + b.date + ' ' + b.time,
    text,
    html,
    reply_to: b.email || undefined,
    attachments: [{ filename: 'm2s-audit.ics', content: b64(internalIcs) }]
  })];

  if (b.email && mailCustomers) {
    const ctext = 'Hi ' + b.name.split(/\s+/)[0] + ',\n\n' +
      'Your free M2S audit with Nuevo Automations is booked for ' + when + '.\n' +
      'It takes about 30 minutes. We will call you on WhatsApp at ' + b.phone + '.\n\n' +
      'A calendar invite is attached. Need a different time? Reply to this email or message us on WhatsApp: https://wa.me/15557738409\n\n' +
      'Nuevo Automations\nhttps://nuevoautomations.com\n';
    const chtml = '<div style="font-family:Inter,Arial,sans-serif;color:#101a2b;font-size:15px;line-height:1.6">' +
      '<p>Hi ' + escapeHtml(b.name.split(/\s+/)[0]) + ',</p>' +
      '<p>Your free M2S audit with Nuevo Automations is booked for <strong>' + escapeHtml(when) + '</strong>.</p>' +
      '<p>It takes about 30 minutes. We will call you on WhatsApp at ' + escapeHtml(b.phone) + '.</p>' +
      '<p>A calendar invite is attached. Need a different time? Reply to this email or ' +
      '<a href="https://wa.me/15557738409" style="color:#1a5fa0">message us on WhatsApp</a>.</p>' +
      '<p style="color:#4b5768">Nuevo Automations<br><a href="https://nuevoautomations.com" style="color:#1a5fa0">nuevoautomations.com</a></p></div>';
    jobs.push(sendMail(env, {
      from,
      to: [b.email],
      subject: 'Your M2S audit is booked — ' + when,
      text: ctext,
      html: chtml,
      reply_to: to,
      attachments: [{ filename: 'nuevo-m2s-audit.ics', content: b64(calendar(null, [customerEvent(b)], 'PUBLISH')) }]
    }));
  }

  const results = await Promise.allSettled(jobs);
  const failed = results.filter((r) => r.status === 'rejected').map((r) => r.reason && r.reason.message);
  if (failed.length) throw new Error(failed.join(' | '));
}

// Short owner notice when a Calendly booking is cancelled or rescheduled
// (a reschedule arrives as a cancel plus a fresh invitee.created).
export async function sendCancelNotice(env, b, rescheduled, reason) {
  if (!env.EMAIL && !env.RESEND_API_KEY) return;
  const what = rescheduled ? 'Rescheduled' : 'Cancelled';
  const lines = [
    what + ': M2S audit with ' + b.name + (b.business ? ' (' + b.business + ')' : '') + ', was ' + prettyWhen(b) + '.',
    rescheduled ? 'The new time arrives as a separate booking.' : null,
    reason ? 'Reason: ' + reason : null,
    'Booking id: ' + b.id
  ].filter(Boolean);
  await sendMail(env, {
    from: env.MAIL_FROM || 'Nuevo Automations <bookings@nuevoautomations.com>',
    to: [env.NOTIFY_EMAIL || 'nawafallahham@nuevoautomations.com'],
    subject: what + ' M2S audit: ' + (b.business || b.name) + ' — ' + b.date + ' ' + b.time,
    text: lines.join('\n') + '\n',
    html: '<div style="font-family:Inter,Arial,sans-serif;color:#101a2b;font-size:15px;line-height:1.5">' +
      lines.map((l) => '<p style="margin:0 0 8px">' + escapeHtml(l) + '</p>').join('') + '</div>',
    reply_to: b.email || undefined
  });
}

// ---- 3. OrcaFlo webhook (WhatsApp confirmation flow) --------------------------
async function sendOrcaflo(env, b) {
  if (!env.ORCAFLO_HOOK_URL || !env.ORCAFLO_HOOK_SECRET) return;
  const r = await fetchWithTimeout(env.ORCAFLO_HOOK_URL, {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + env.ORCAFLO_HOOK_SECRET, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: b.id, date: b.date, time: b.time, tz: 'Asia/Dubai',
      starts_at: slotInstant(b.date, b.time).toISOString(),
      name: b.name, phone: b.phone, business: b.business, email: b.email,
      source: b.source, provider: b.provider || 'native', utm_source: b.utm_source, utm_campaign: b.utm_campaign, utm_content: b.utm_content
    })
  }, 5000);
  if (!r.ok) throw new Error('OrcaFlo ' + r.status + ': ' + (await r.text()).slice(0, 300));
}

export async function fetchWithTimeout(url, init, ms) {
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), ms);
  try {
    return await fetch(url, { ...init, signal: ac.signal });
  } finally {
    clearTimeout(t);
  }
}
