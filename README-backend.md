# Backend: Cloudflare Worker + D1

One Worker (`worker/index.js`) serves the static site from this folder (Workers static assets) plus `/api/*`. Data lives in the D1 database `nuevo-site`.

| Path | What it does |
|---|---|
| `POST /api/calendly/webhook` | Calendly `invitee.created` / `invitee.canceled` (signed with `CALENDLY_SIGNING_KEY`) |
| `POST /api/calendly/scheduled` | Browser beacon from `js/calendly.js` after a Calendly booking (consent + attribution) |
| `GET /api/slots?days=14` | Native slot picker: taken slots per date. Unused by the site since Calendly |
| `POST /api/book` | Native booking (validation, honeypot, 5/hour/IP limit, 409 on a taken slot). Unused since Calendly |
| `POST /api/track` | Anonymous, cookieless analytics beacon (from `js/track.js`) |
| `GET /api/calendar.ics?key=…` | Private iCal feed for Google Calendar |
| `/api/admin/*` | Dashboard API (`Authorization: Bearer ADMIN_KEY`), UI at `/admin/` |

After each booking (native or Calendly) these run in the background and are skipped when their secrets aren't set: Meta CAPI `Schedule` (only if the visitor accepted cookies), Resend email alert with an .ics (plus a confirmation to the customer if they gave an email), and the OrcaFlo webhook.

A nightly cron (23:17 UTC) deletes bookings 90 days after their date, analytics events older than 400 days, stale rate-limit rows, and Calendly beacon rows older than 2 days. The privacy policy depends on this.

## Files
- `wrangler.toml`: config. **`database_id` is a placeholder.** The custom-domain `routes` are commented out.
- `worker/`: `index.js` (router + cron), `api.js`, `calendly.js`, `admin.js`, `notify.js` (CAPI/email/OrcaFlo), `ics.js`, `lib.js`
- `migrations/0001_init.sql`: tables `bookings`, `events`, `rate`
- `migrations/0002_calendly.sql`: Calendly columns on `bookings`, table `calendly_pending`
- `_headers`, `_redirects`, `.assetsignore`: static asset config (the ignore list keeps worker/, migrations/, booking-api/ and similar folders from being published)
- `admin/index.html`: private dashboard (noindex, not linked)
- `js/track.js`, `js/calendly.js`: front end (`js/booking.js` is the old native picker, no longer loaded)
- `booking-api/`: the old Vercel + Upstash API, no longer used. Delete it after cut-over.

## First deploy
```sh
npm install
npx wrangler login
npx wrangler d1 create nuevo-site          # paste the printed database_id into wrangler.toml
npx wrangler d1 migrations apply nuevo-site --remote

# secrets (each prompts for the value)
npx wrangler secret put ADMIN_KEY          # long random string, e.g. `openssl rand -hex 24`
npx wrangler secret put CALENDAR_KEY       # another long random string
npx wrangler secret put HASH_SALT          # optional but recommended: random string for IP/visitor hashing
npx wrangler secret put META_CAPI_TOKEN    # Events Manager > Settings > Conversions API > Generate access token
npx wrangler secret put RESEND_API_KEY     # nuevoautomations.com must be a verified domain in Resend
npx wrangler secret put ORCAFLO_HOOK_URL
npx wrangler secret put ORCAFLO_HOOK_SECRET
npx wrangler secret put CALENDLY_TOKEN       # Calendly personal access token (see "Calendly" below)
npx wrangler secret put CALENDLY_SIGNING_KEY # long random string, e.g. `openssl rand -hex 32`
# optional:
npx wrangler secret put MAIL_FROM          # default "Nuevo Automations <bookings@nuevoautomations.com>"
npx wrangler secret put META_TEST_EVENT_CODE   # only while testing in Events Manager; delete afterwards

npx wrangler deploy                        # goes to https://nuevo-site.<account>.workers.dev
```
`META_PIXEL_ID`, `NOTIFY_EMAIL` and `SITE_URL` are plain `[vars]` in `wrangler.toml`. To override `NOTIFY_EMAIL`, edit it there or delete it from `[vars]` and set it as a secret.

### Go live on the domain
1. The zone `nuevoautomations.com` must be on Cloudflare. In DNS, delete the old Vercel `A`/`CNAME` records for `@` and `www`.
2. Uncomment `routes` in `wrangler.toml`, then run `npx wrangler deploy`. Cloudflare creates the DNS records and certificates. The Worker 301s `www` to the apex.
3. In Meta Events Manager, test with `META_TEST_EVENT_CODE`, then delete that secret: `npx wrangler secret delete META_TEST_EVENT_CODE`.
4. Open `/admin/`, sign in with `ADMIN_KEY`, and copy the calendar URL into Google Calendar (Other calendars → From URL).

## Calendly
Calendly is the scheduler (event `https://calendly.com/nawaf-allahham02/30min`). `/book/` and `/consultation/` embed it inline via `js/calendly.js`, which passes the visitor's first-touch `utm_*` to Calendly. Each booking still lands in the `bookings` table (`provider = 'calendly'`) and triggers the email alert, OrcaFlo hook and calendar feed exactly like a native booking. Calendly sends the customer's confirmation, so we don't email the customer for Calendly bookings.

How a booking arrives:
1. Calendly's webhook (`invitee.created`) to `/api/calendly/webhook`. The signature is checked (HMAC-SHA256, max 5 minutes old) and the event is idempotent on the invitee URI. Start time is stored as Dubai date/time. The answer to a question matching *whatsapp/phone/mobile* becomes the phone (else Calendly's text-reminder number), *business/company* becomes the business, and the other answers go into the note. `invitee.canceled` (including reschedules, which arrive as a cancel plus a new `invitee.created`) marks the row cancelled and emails a short notice.
2. The browser beacon `/api/calendly/scheduled` carries cookie consent, attribution and Meta's `fbc`/`fbp`.

Meta CAPI `Schedule` (event_id = the Calendly invitee URI, matching the browser pixel) is sent only when the beacon said consent was granted, by whichever of the two arrives second, and at most once (`capi_sent_at`). Logs: `[calendly] capi …`.

**Setup** (needs a paid Calendly plan, since webhooks aren't on the free plan):
1. Calendly → Integrations → API and webhooks → create a personal access token. Then `npx wrangler secret put CALENDLY_TOKEN`.
2. `openssl rand -hex 32 | npx wrangler secret put CALENDLY_SIGNING_KEY`
3. Apply the migration and deploy: `npx wrangler d1 migrations apply nuevo-site --remote && npx wrangler deploy`.
4. Open `/admin/` → Calendly → **Connect Calendly webhook**. This deletes any existing subscription for our callback URL and creates a new one for `invitee.created` and `invitee.canceled`. If Calendly refuses (for example on the free plan), its error is shown there. Click it again after rotating `CALENDLY_SIGNING_KEY`.
5. In the Calendly event, add a required question such as "WhatsApp number" and an optional "Business name", so the phone and business columns get filled.

## Local development
```sh
printf 'ADMIN_KEY="local-admin"\nCALENDAR_KEY="local-cal"\n' > .dev.vars   # gitignored
npx wrangler d1 migrations apply nuevo-site --local
npx wrangler dev --local --port 8787
```
To try the Calendly webhook locally, add `CALENDLY_SIGNING_KEY="test"` to `.dev.vars` and sign the body yourself: header `Calendly-Webhook-Signature: t=<unix>,v1=<hex HMAC-SHA256("test", t + "." + body)>`.
Local D1 data lives in `.wrangler/` (gitignored).

## Ops snippets
```sh
# upcoming bookings
npx wrangler d1 execute nuevo-site --remote --command "SELECT date,time,name,phone,business,status FROM bookings WHERE date >= date('now') ORDER BY date,time"
# live logs (side-effect failures are logged as [meta_capi] / [email] / [orcaflo])
npx wrangler tail
```
Rotating `ADMIN_KEY` or `CALENDAR_KEY`: `wrangler secret put` the new value. Rotating `CALENDAR_KEY` means re-subscribing to the calendar URL in Google Calendar.
