// Minimal iCalendar (RFC 5545) builder. All times are written in UTC, so no
// VTIMEZONE block is needed; calendar apps convert to local time.
import { slotInstant, meetingMinutes, waLink } from './lib.js';

function stamp(d) {
  return d.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
}

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,')
    .replace(/\r?\n/g, '\\n');
}

// Fold lines at 75 octets (continuation lines start with a space).
function fold(line) {
  const bytes = new TextEncoder().encode(line);
  if (bytes.length <= 75) return line;
  const out = [];
  let cur = '', curLen = 0, limit = 75;
  for (const ch of line) {
    const n = new TextEncoder().encode(ch).length;
    if (curLen + n > limit) {
      out.push(cur);
      cur = ' '; curLen = 1; limit = 75;
    }
    cur += ch; curLen += n;
  }
  out.push(cur);
  return out.join('\r\n');
}

export function vevent({ uid, date, time, minutes, summary, description, location, url, created }) {
  const start = slotInstant(date, time);
  const end = new Date(start.getTime() + minutes * 60 * 1000);
  const lines = [
    'BEGIN:VEVENT',
    'UID:' + uid + '@nuevoautomations.com',
    'DTSTAMP:' + stamp(created ? new Date(created) : new Date()),
    'DTSTART:' + stamp(start),
    'DTEND:' + stamp(end),
    'SUMMARY:' + esc(summary),
    'DESCRIPTION:' + esc(description)
  ];
  if (location) lines.push('LOCATION:' + esc(location));
  if (url) lines.push('URL:' + url);
  lines.push('STATUS:CONFIRMED', 'END:VEVENT');
  return lines;
}

export function calendar(name, events, method) {
  const lines = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//Nuevo Automations//Bookings//EN',
    'CALSCALE:GREGORIAN'
  ];
  if (method) lines.push('METHOD:' + method);
  if (name) lines.push('X-WR-CALNAME:' + esc(name), 'X-WR-TIMEZONE:Asia/Dubai', 'REFRESH-INTERVAL;VALUE=DURATION:PT1H', 'X-PUBLISHED-TTL:PT1H');
  events.forEach((e) => lines.push(...e));
  lines.push('END:VCALENDAR');
  return lines.map(fold).join('\r\n') + '\r\n';
}

// Event as Nawaf sees it (feed + alert email).
export function internalEvent(b) {
  return vevent({
    uid: b.id,
    date: b.date,
    time: b.time,
    minutes: meetingMinutes(b),
    created: b.created_at,
    summary: 'M2S audit — ' + (b.business || b.name),
    description: [
      'Name: ' + b.name,
      b.business ? 'Business: ' + b.business : null,
      b.phone ? 'WhatsApp: ' + b.phone : null,
      b.phone ? 'Chat: ' + waLink(b.phone) : null,
      b.email ? 'Email: ' + b.email : null,
      'Source: ' + [b.source, b.utm_source, b.utm_campaign].filter(Boolean).join(' / '),
      b.note ? 'Note: ' + b.note : null,
      b.reschedule_url ? 'Reschedule: ' + b.reschedule_url : null,
      b.cancel_url ? 'Cancel: ' + b.cancel_url : null
    ].filter(Boolean).join('\n'),
    location: b.phone ? 'WhatsApp call ' + b.phone : 'Calendly booking'
  });
}

// Event as the customer sees it (confirmation email).
export function customerEvent(b) {
  return vevent({
    uid: b.id + '-c',
    date: b.date,
    time: b.time,
    minutes: meetingMinutes(b),
    created: b.created_at,
    summary: 'Free M2S audit with Nuevo Automations',
    description: 'Your free 30-minute M2S (Message to Sale) audit with Nuevo Automations. ' +
      'We will call you on WhatsApp at ' + b.phone + '.\n' +
      'Need to change the time? Message us: https://wa.me/971508549171',
    location: 'WhatsApp call',
    url: 'https://nuevoautomations.com/'
  });
}
